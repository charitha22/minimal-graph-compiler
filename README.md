# mgc — Minimal Graph Compiler

A minimal MLIR-based compiler, currently providing a single tool `mgc-opt` that parses,
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