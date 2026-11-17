# mgc — Minimal Graph Compiler

A minimal MLIR-based compiler, providing `mgc-opt` (a small `mlir-opt` clone)
and a Python runtime (`mgc`) for executing LLVM-dialect modules with the MLIR
execution engine.

## Building

### Prerequisites

- A recent **LLVM/MLIR** build (version 18 or later recommended).
- CMake ≥ 3.20.
- A C++17-capable compiler.
- **FileCheck** (ships with LLVM) — needed to run tests.

### Configure & build

```sh
cmake -B build -DLLVM_BUILD_DIR=/path/to/llvm-project/build
cmake --build build
```

The `mgc-opt` binary is placed in `build/bin/`.

## Running tests

Use the `check-mgc` target to run all tests:

```sh
cmake --build build --target check-mgc
```

This runs `mgc-opt` on each test file in `test/` and verifies the output with
**FileCheck**.

You can also run a single test manually:

```sh
mgc-opt test/check-mgc-opt.mlir | FileCheck test/check-mgc-opt.mlir
```

## Python runtime

`python/mgc` executes LLVM-dialect MLIR modules through the MLIR Python
bindings.

### Install

Development (editable):

```sh
python -m pip install -e python/
```

Normal install:

```sh
python -m pip install ./python
```

### MLIR bindings

If `import mlir` already works, nothing else is needed. Otherwise point mgc at
the LLVM build:

```sh
export LLVM_BUILD_DIR=/path/to/llvm-project/build
```

### Usage

Given an MLIR string that is already lowered to the LLVM dialect:

```python
import numpy as np
from mgc import Executor

with Executor.from_llvm_mlir(llvm_mlir_text) as executor:
    a = np.full((4, 4), 1.11, dtype=np.float32)
    b = np.full((4, 4), 2.22, dtype=np.float32)
    c = np.zeros((4, 4), dtype=np.float32)
    executor.invoke("matmul", a, b, c)

np.testing.assert_allclose(c, a @ b, rtol=1e-5, atol=1e-3)
```

`Executor.from_file("module.mlir")` reads the same LLVM-dialect IR from disk.

### Tests

```sh
cmake --build build --target check-mgc-python
```

`check-mgc` already runs the Python tests too.
