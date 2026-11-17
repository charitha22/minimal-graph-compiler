"""mgc — Python runtime for the minimal graph compiler.

The package executes MLIR modules that are already in the LLVM dialect using
the MLIR Python execution engine.

Example::

    import numpy as np
    from mgc import Executor

    with Executor.from_file("kernel-llvm.mlir") as executor:
        a = np.full((512, 512), 1.11, dtype=np.float32)
        b = np.full((512, 512), 2.22, dtype=np.float32)
        c = np.zeros((512, 512), dtype=np.float32)
        executor.invoke("matmul", a, b, c)
"""

from .execution import Executor
from .memref import f32, f64, i32, i64, index

__all__ = [
    "Executor",
    "f32",
    "f64",
    "i32",
    "i64",
    "index",
]

__version__ = "0.1.0"
