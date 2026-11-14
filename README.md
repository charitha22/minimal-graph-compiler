# gc — Minimal Graph Compiler

A minimal MLIR-based compiler, currently providing a single tool `gc-opt` that parses,
optimises, and prints MLIR modules.

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

The `gc-opt` binary is placed in `build/bin/`.

## Running tests

Use the `check-gc` target to run all tests:

```sh
cmake --build build --target check-gc
```

This runs `gc-opt` on each test file in `test/` and verifies the output with
**FileCheck**.

You can also run a single test manually:

```sh
gc-opt test/check-gc-opt.mlir | FileCheck test/check-gc-opt.mlir
```