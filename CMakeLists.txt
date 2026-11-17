cmake_minimum_required(VERSION 3.20)

project(mgc LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

enable_testing()

# Optional: the mgc Python runtime package (python/mgc).  It wraps the MLIR
# Python bindings from the same LLVM build used for mgc-opt.
option(MGC_ENABLE_PYTHON "Enable the mgc Python runtime package" ON)

# LLVM_BUILD_DIR must be provided on the command line:
#   -DLLVM_BUILD_DIR=/path/to/llvm-project/build
set(MLIR_DIR "${LLVM_BUILD_DIR}/lib/cmake/mlir" CACHE PATH
    "Path to the MLIR CMake package")

find_package(LLVM REQUIRED CONFIG
    PATHS "${LLVM_BUILD_DIR}/lib/cmake/llvm" NO_DEFAULT_PATH)
find_package(MLIR REQUIRED CONFIG)

message(STATUS "Using LLVM from ${LLVM_BUILD_DIR}")
message(STATUS "Using MLIR from ${MLIR_DIR}")

include_directories(${LLVM_INCLUDE_DIRS} ${MLIR_INCLUDE_DIRS})
link_directories(${LLVM_BUILD_LIBRARY_DIR})
add_definitions(${LLVM_DEFINITIONS})

list(APPEND CMAKE_MODULE_PATH "${LLVM_BUILD_DIR}/lib/cmake/llvm")
include(AddLLVM)

add_subdirectory(lib)
add_subdirectory(tools)
add_subdirectory(test)

if(MGC_ENABLE_PYTHON)
  add_subdirectory(python)
endif()
