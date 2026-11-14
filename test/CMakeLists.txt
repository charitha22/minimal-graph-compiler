set(MGC_TEST_DEPS mgc-opt)

add_lit_target(check-mgc
  "Running mgc regression tests"
  "${CMAKE_CURRENT_SOURCE_DIR}"
  ARGS --param gc_tools_dir=${CMAKE_BINARY_DIR}/bin
       --param gc_obj_root=${CMAKE_CURRENT_BINARY_DIR}
       --param llvm_tools_dir=${LLVM_TOOLS_BINARY_DIR}
  DEPENDS ${MGC_TEST_DEPS}
)