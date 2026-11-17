"""Execution of LLVM-dialect MLIR modules from Python."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence

from . import _env

_env.ensure_mlir_bindings()

from mlir import ir  # noqa: E402
from mlir.execution_engine import ExecutionEngine  # noqa: E402

from .memref import as_arg  # noqa: E402


class Executor:
    """Wraps an MLIR execution engine with NumPy-friendly invocation.

    The module must already be in the LLVM dialect (i.e. translatable to LLVM
    IR).  Use your normal lowering driver (e.g. ``mgc-opt`` or ``mlir-opt``)
    to produce it.
    """

    def __init__(
        self,
        module: ir.Module,
        *,
        context: ir.Context | None = None,
        shared_libs: Sequence[str] | None = None,
        opt_level: int = 3,
    ) -> None:
        self._module = module
        self._context = context if context is not None else module.context
        libraries = (
            _env.default_shared_libs() if shared_libs is None else list(shared_libs)
        )
        self._engine = ExecutionEngine(
            module,
            opt_level=opt_level,
            shared_libs=libraries,
        )

    @classmethod
    def from_llvm_mlir(
        cls,
        source: str,
        *,
        shared_libs: Sequence[str] | None = None,
        opt_level: int = 3,
    ) -> "Executor":
        """Create an executor from LLVM-dialect MLIR text."""
        with ir.Context() as context, ir.Location.unknown():
            module = ir.Module.parse(source)
            return cls(
                module,
                context=context,
                shared_libs=shared_libs,
                opt_level=opt_level,
            )

    @classmethod
    def from_file(
        cls,
        path: str | os.PathLike[str],
        *,
        shared_libs: Sequence[str] | None = None,
        opt_level: int = 3,
    ) -> "Executor":
        """Create an executor from an LLVM-dialect MLIR file."""
        return cls.from_llvm_mlir(
            Path(path).read_text(),
            shared_libs=shared_libs,
            opt_level=opt_level,
        )

    def invoke(self, name: str, *args: object) -> None:
        """Invoke a C-interface function (``_mlir_ciface_<name>``)."""
        packed_args = []
        keepalive = []
        for arg in args:
            packed, alive = as_arg(arg)
            packed_args.append(packed)
            keepalive.append(alive)
        self._engine.invoke(name, *packed_args)
        # Keep descriptors alive until after the call.
        del keepalive

    def __enter__(self) -> "Executor":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self._engine = None

    def __repr__(self) -> str:
        return f"<mgc.Executor module={self._module!r}>"
