"""Tests for the mgc Python runtime.

The tests start from a small linalg.matmul, lower it to the LLVM dialect with
the MLIR Python pass manager, and then execute it through mgc.Executor.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from mgc import Executor  # importing mgc also bootstraps the MLIR bindings path

from mlir import ir
from mlir.passmanager import PassManager

SIZE = 4

MATMUL_SOURCE = f"""
func.func @matmul(%A: memref<{SIZE}x{SIZE}xf32>,
                  %B: memref<{SIZE}x{SIZE}xf32>,
                  %C: memref<{SIZE}x{SIZE}xf32>) attributes {{llvm.emit_c_interface}} {{
  linalg.matmul ins(%A, %B: memref<{SIZE}x{SIZE}xf32>, memref<{SIZE}x{SIZE}xf32>)
                outs(%C: memref<{SIZE}x{SIZE}xf32>)
  return
}}
"""

LOWERING_PIPELINE = "builtin.module(" + ",".join(
    (
        "convert-linalg-to-loops",
        "convert-scf-to-cf",
        "expand-strided-metadata",
        "lower-affine",
        "convert-arith-to-llvm",
        "convert-math-to-llvm",
        "convert-vector-to-llvm",
        "finalize-memref-to-llvm",
        "convert-func-to-llvm",
        "convert-cf-to-llvm",
        "reconcile-unrealized-casts",
    )
) + ")"


def lower_to_llvm(source: str) -> str:
    with ir.Context() as context, ir.Location.unknown():
        module = ir.Module.parse(source)
        PassManager.parse(LOWERING_PIPELINE).run(module.operation)
        return str(module)


class MatmulTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lowered = lower_to_llvm(MATMUL_SOURCE)

    def _inputs(self):
        a = np.full((SIZE, SIZE), 1.11, dtype=np.float32)
        b = np.full((SIZE, SIZE), 2.22, dtype=np.float32)
        c = np.zeros((SIZE, SIZE), dtype=np.float32)
        return a, b, c

    def test_from_llvm_mlir_text(self):
        a, b, c = self._inputs()
        with Executor.from_llvm_mlir(self.lowered) as executor:
            executor.invoke("matmul", a, b, c)

        np.testing.assert_allclose(c, a @ b, rtol=1e-5, atol=1e-3)

    def test_from_file(self):
        a, b, c = self._inputs()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "matmul-llvm.mlir"
            path.write_text(self.lowered)
            with Executor.from_file(path) as executor:
                executor.invoke("matmul", a, b, c)

        np.testing.assert_allclose(c, a @ b, rtol=1e-5, atol=1e-3)

    def test_rejects_non_contiguous_memref(self):
        a, b, c = self._inputs()
        a = np.asfortranarray(a)
        with Executor.from_llvm_mlir(self.lowered) as executor:
            with self.assertRaises(ValueError):
                executor.invoke("matmul", a, b, c)


if __name__ == "__main__":
    unittest.main()
