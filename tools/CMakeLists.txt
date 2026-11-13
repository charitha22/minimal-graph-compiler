add_executable(gc-opt gc-opt.cpp)

target_include_directories(gc-opt PRIVATE "${PROJECT_SOURCE_DIR}/include")

# Match the LLVM/MLIR build configuration (LLVM is built without RTTI).
target_compile_options(gc-opt PRIVATE -fno-rtti)

target_link_libraries(gc-opt PRIVATE
  MLIRIR
  MLIRParser
  MLIRPass
  MLIRSupport
  MLIRArithDialect
  MLIRControlFlowDialect
  MLIRFuncDialect
  MLIRSCFDialect
)
