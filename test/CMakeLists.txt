set(GC_TEST_DEPS gc-opt)

add_lit_target(check-gc
  "Running gc regression tests"
  "${CMAKE_CURRENT_SOURCE_DIR}"
  ARGS --param gc_tools_dir=${CMAKE_BINARY_DIR}/bin
       --param gc_obj_root=${CMAKE_CURRENT_BINARY_DIR}
       --param llvm_tools_dir=${LLVM_TOOLS_BINARY_DIR}
  DEPENDS ${GC_TEST_DEPS}
)