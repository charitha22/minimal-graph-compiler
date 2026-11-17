# Python runtime package (mgc).
#
# This is a pure-Python package: it wraps the MLIR Python bindings from the
# LLVM build that mgc is configured against.  There is no compiled extension.

find_package(Python3 COMPONENTS Interpreter REQUIRED)

set(MGC_MLIR_PYTHON_PACKAGE
    "${LLVM_BUILD_DIR}/tools/mlir/python_packages/mlir_core"
    CACHE PATH "Path to the MLIR Python bindings package (mlir_core)")

if(NOT EXISTS "${MGC_MLIR_PYTHON_PACKAGE}/mlir")
  message(WARNING
    "MLIR Python bindings not found at ${MGC_MLIR_PYTHON_PACKAGE}.\n"
    "Set -DMGC_MLIR_PYTHON_PACKAGE=<llvm-build>/tools/mlir/python_packages/mlir_core "
    "or configure with -DMGC_ENABLE_PYTHON=OFF.")
endif()

set(MGC_PYTHON_TEST_ENV
  "PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}:${MGC_MLIR_PYTHON_PACKAGE}"
  "LLVM_BUILD_DIR=${LLVM_BUILD_DIR}"
  "MGC_MLIR_PYTHON_PACKAGE=${MGC_MLIR_PYTHON_PACKAGE}")

add_custom_target(check-mgc-python
  COMMAND ${CMAKE_COMMAND} -E env ${MGC_PYTHON_TEST_ENV}
          ${Python3_EXECUTABLE} -m unittest discover -v
          --start-directory "${CMAKE_CURRENT_SOURCE_DIR}/tests"
          --top-level-directory "${CMAKE_CURRENT_SOURCE_DIR}"
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  DEPENDS mgc-opt
  USES_TERMINAL
  COMMENT "Running mgc Python runtime tests")

add_test(NAME mgc-python
  COMMAND ${CMAKE_COMMAND} -E env ${MGC_PYTHON_TEST_ENV}
          ${Python3_EXECUTABLE} -m unittest discover -v
          --start-directory "${CMAKE_CURRENT_SOURCE_DIR}/tests"
          --top-level-directory "${CMAKE_CURRENT_SOURCE_DIR}")
set_tests_properties(mgc-python PROPERTIES
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")

# Make the main regression target cover the Python runtime as well.
if(TARGET check-mgc)
  add_dependencies(check-mgc check-mgc-python)
endif()

include(GNUInstallDirs)
set(MGC_PYTHON_INSTALL_DIR
    "${CMAKE_INSTALL_LIBDIR}/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages")

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/mgc"
        DESTINATION "${MGC_PYTHON_INSTALL_DIR}"
        COMPONENT python
        PATTERN "__pycache__" EXCLUDE
        PATTERN "*.pyc" EXCLUDE)
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/pyproject.toml"
        DESTINATION "${MGC_PYTHON_INSTALL_DIR}"
        COMPONENT python)
