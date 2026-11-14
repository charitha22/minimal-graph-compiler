add_executable(mgc-opt mgc-opt.cpp)

target_include_directories(mgc-opt PRIVATE "${PROJECT_SOURCE_DIR}/include")

# Match the LLVM/MLIR build configuration (LLVM is built without RTTI).
target_compile_options(mgc-opt PRIVATE -fno-rtti)

target_link_libraries(mgc-opt PRIVATE
  MLIRIR
  MLIRParser
  MLIRPass
  MLIRSupport
  MLIRArithDialect
  MLIRControlFlowDialect
  MLIRFuncDialect
  MLIRSCFDialect
)
