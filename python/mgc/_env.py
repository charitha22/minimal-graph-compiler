"""Discovery helpers for the upstream MLIR Python bindings and runtime libs.

``mgc`` intentionally does not build its own Python extension.  It wraps the
MLIR Python bindings that ship with the LLVM/MLIR build that mgc is already
configured against.  This keeps the build simple and guarantees that the
bindings, C API and JIT use the same LLVM build as ``mgc-opt``.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


def ensure_mlir_bindings() -> None:
    """Make sure ``import mlir`` works, or raise a useful error.

    The package is searched for in this order:

    1. ``MGC_MLIR_PYTHON_PACKAGE``
    2. ``MLIR_PYTHON_PACKAGE``
    3. ``$LLVM_BUILD_DIR/tools/mlir/python_packages/mlir_core``
    """
    if importlib.util.find_spec("mlir") is not None:
        return

    candidates: list[Path] = []
    for var in ("MGC_MLIR_PYTHON_PACKAGE", "MLIR_PYTHON_PACKAGE"):
        value = os.environ.get(var)
        if value:
            candidates.append(Path(value))

    llvm_build_dir = os.environ.get("LLVM_BUILD_DIR")
    if llvm_build_dir:
        candidates.append(
            Path(llvm_build_dir) / "tools" / "mlir" / "python_packages" / "mlir_core"
        )

    for candidate in candidates:
        if (candidate / "mlir").is_dir():
            sys.path.insert(0, str(candidate))
            return

    raise ImportError(
        "could not import the MLIR Python bindings.\n"
        "Point MGC_MLIR_PYTHON_PACKAGE (or LLVM_BUILD_DIR) at the LLVM build "
        "that contains tools/mlir/python_packages/mlir_core."
    )


def _runner_util_names() -> tuple[str, ...]:
    return ("libmlir_c_runner_utils", "libmlir_runner_utils")


def _library_dirs() -> list[Path]:
    dirs: list[Path] = []

    if os.environ.get("MGC_SHARED_LIBS"):
        # Explicit paths take precedence.
        return dirs

    llvm_build_dir = os.environ.get("LLVM_BUILD_DIR")
    if llvm_build_dir:
        dirs.append(Path(llvm_build_dir) / "lib")

    # If the MLIR bindings come from an LLVM build tree (or an install where
    # the runtime libraries live next to the Python packages), derive the
    # library directory from the imported ``mlir`` package.
    try:
        import mlir
    except ImportError:
        return dirs

    # ``mlir`` can be a regular package (has __file__) or a namespace package
    # in the LLVM build tree (only has __path__).
    mlir_paths: list[Path] = []
    mlir_module_file = getattr(mlir, "__file__", None)
    if mlir_module_file:
        mlir_paths.append(Path(mlir_module_file).resolve())
    for package_path in getattr(mlir, "__path__", ()):  # type: ignore[arg-type]
        mlir_paths.append(Path(package_path).resolve())

    for mlir_path in mlir_paths:
        for parent in mlir_path.parents:
            candidate = parent / "lib"
            has_runner_utils = any(
                (candidate / f"{name}{suffix}").exists()
                for name in _runner_util_names()
                for suffix in (".so", ".dylib")
            )
            if has_runner_utils:
                if candidate not in dirs:
                    dirs.append(candidate)
                break
    return dirs


def default_shared_libs() -> list[str]:
    """Return the MLIR runner utility libraries for the execution engine.

    Override with ``MGC_SHARED_LIBS`` (an ``os.pathsep``-separated list of
    library paths) when using an unusual LLVM layout.
    """
    explicit = os.environ.get("MGC_SHARED_LIBS")
    if explicit:
        return [path for path in explicit.split(os.pathsep) if path]

    found: list[str] = []
    for directory in _library_dirs():
        for name in _runner_util_names():
            for suffix in (".so", ".dylib"):
                candidate = directory / f"{name}{suffix}"
                if candidate.exists():
                    found.append(str(candidate))
                    break
        if found:
            return found
    return found

