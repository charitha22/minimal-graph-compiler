cmake_minimum_required(VERSION 3.20)

project(gc LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

# Point this at the directory containing MLIRConfig.cmake. Override on the
# command line with -DMLIR_DIR=/path/to/llvm-project/build/lib/cmake/mlir.
if(NOT DEFINED MLIR_DIR)
  get_filename_component(
    _GC_DEFAULT_MLIR_DIR
    "${CMAKE_CURRENT_SOURCE_DIR}/../llvm-project/build/lib/cmake/mlir"
    ABSOLUTE)
  set(MLIR_DIR "${_GC_DEFAULT_MLIR_DIR}" CACHE PATH
      "Path to the MLIR CMake package")
endif()

find_package(MLIR REQUIRED CONFIG)

message(STATUS "Using MLIR from ${MLIR_DIR}")

include_directories(${LLVM_INCLUDE_DIRS} ${MLIR_INCLUDE_DIRS})
link_directories(${LLVM_BUILD_LIBRARY_DIR})
add_definitions(${LLVM_DEFINITIONS})

add_subdirectory(lib)
add_subdirectory(tools)
