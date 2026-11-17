"""Conversion of NumPy arrays and scalars to execution engine arguments."""

from __future__ import annotations

import ctypes
from typing import Any

import numpy as np

from mlir.runtime import get_ranked_memref_descriptor


def f32(value: float) -> ctypes.c_float:
    """An f32 scalar argument."""
    return ctypes.c_float(value)


def f64(value: float) -> ctypes.c_double:
    """An f64 scalar argument."""
    return ctypes.c_double(value)


def i32(value: int) -> ctypes.c_int32:
    """An i32 scalar argument."""
    return ctypes.c_int32(value)


def i64(value: int) -> ctypes.c_int64:
    """An i64 scalar argument."""
    return ctypes.c_int64(value)


def index(value: int) -> ctypes.c_ssize_t:
    """An ``index`` scalar argument (pointer-sized integer)."""
    return ctypes.c_ssize_t(value)


def as_arg(arg: Any) -> tuple[Any, Any]:
    """Pack one Python value for ``ExecutionEngine.invoke``.

    Returns ``(invoke_arg, keepalive)``.  ``keepalive`` must stay alive until
    the call returns because it owns the memory referenced by ``invoke_arg``.

    Supported values:

    * ``numpy.ndarray``: passed as a ranked memref descriptor.
    * ``ctypes`` scalar/structure: passed by pointer.
    * anything else: assumed to be an already packed pointer.
    """
    if isinstance(arg, np.ndarray):
        if not arg.flags.c_contiguous:
            raise ValueError(
                "memref arguments must be C-contiguous; "
                "call numpy.ascontiguousarray() first"
            )
        descriptor = get_ranked_memref_descriptor(arg)
        # MLIR's C interface wrappers expect a pointer to a pointer to the
        # descriptor (the packed argument is a void**).
        descriptor_ptr = ctypes.pointer(descriptor)
        arg_ptr = ctypes.pointer(descriptor_ptr)
        return arg_ptr, (descriptor, descriptor_ptr, arg_ptr)

    if isinstance(arg, np.generic):
        ctype = np.ctypeslib.as_ctypes_type(arg.dtype)
        value = ctype(arg.item())
        arg_ptr = ctypes.pointer(value)
        return arg_ptr, (value, arg_ptr)

    if isinstance(arg, ctypes._SimpleCData) or isinstance(
        arg, (ctypes.Structure, ctypes.Union)
    ):
        arg_ptr = ctypes.pointer(arg)
        return arg_ptr, (arg, arg_ptr)

    return arg, arg
