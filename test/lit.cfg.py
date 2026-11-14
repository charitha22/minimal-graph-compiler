# -*- Python -*-

import os

import lit.formats
import lit.llvm

# Initialize the LLVM config helper.
lit.llvm.initialize(lit_config, config)
from lit.llvm import llvm_config

# name: The name of this test suite.
config.name = "GC"

# test_format: Use ShTest (the standard lit shell test format).
config.test_format = lit.formats.ShTest()

# suffixes: Which file extensions are tests.
config.suffixes = [".mlir"]

# test_source_root: Where tests are located.
config.test_source_root = os.path.dirname(__file__)

# test_exec_root: Where tests should be run.
config.test_exec_root = lit_config.params.get("gc_obj_root", config.test_source_root)

# excludes: Directories/files to ignore.
config.excludes = ["CMakeLists.txt", "lit.cfg.py"]

# Tweak the PATH to include the build's tools directory.
gc_tools_dir = lit_config.params.get("gc_tools_dir", "")
llvm_tools_dir = lit_config.params.get("llvm_tools_dir", "")
tool_dirs = [d for d in [gc_tools_dir, llvm_tools_dir] if d]
for d in tool_dirs:
    llvm_config.with_environment("PATH", d, append_path=True)

# Register available tools.
tools = [
    "FileCheck",
    "gc-opt",
]
llvm_config.add_tool_substitutions(tools, tool_dirs)