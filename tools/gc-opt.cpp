//===- gc-opt.cpp - Minimal MLIR optimizer driver -------------------------===//
//
// A tiny mlir-opt clone: read an MLIR file, parse it, run an (initially
// empty) pass pipeline, then print the result.
//
//===----------------------------------------------------------------------===//

#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/ControlFlow/IR/ControlFlowOps.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/IR/AsmState.h"
#include "mlir/IR/BuiltinOps.h"
#include "mlir/IR/DialectRegistry.h"
#include "mlir/IR/MLIRContext.h"
#include "mlir/Parser/Parser.h"
#include "mlir/Pass/PassManager.h"
#include "mlir/Pass/PassRegistry.h"

#include "llvm/Support/CommandLine.h"
#include "llvm/Support/InitLLVM.h"
#include "llvm/Support/raw_ostream.h"

using namespace mlir;

static llvm::cl::opt<std::string> inputFilename(
    llvm::cl::Positional, llvm::cl::desc("<input file>"), llvm::cl::init("-"));

int main(int argc, char **argv) {
  llvm::InitLLVM initLLVM(argc, argv);

  // Register the usual MLIR command-line options: -mlir-print-ir-after-all,
  // -mlir-print-op-generic, -pass-pipeline, etc.
  registerAsmPrinterCLOptions();
  registerMLIRContextCLOptions();
  registerPassManagerCLOptions();
  PassPipelineCLParser passPipeline("", "Compiler passes to run", "p");

  llvm::cl::ParseCommandLineOptions(
      argc, argv, "gc-opt - minimal MLIR optimizer driver\n");

  // Register the dialects this tool understands.
  DialectRegistry registry;
  registry.insert<arith::ArithDialect, cf::ControlFlowDialect,
                  func::FuncDialect, scf::SCFDialect>();

  MLIRContext context(registry);
  context.loadAllAvailableDialects();

  // Parse the input (a filename, or "-" for stdin).
  OwningOpRef<ModuleOp> module = parseSourceFile<ModuleOp>(
      inputFilename.getValue(), ParserConfig(&context));
  if (!module)
    return 1;

  // Build and run the pass pipeline.
  PassManager pm(&context);
  if (failed(applyPassManagerCLOptions(pm)))
    return 1;

  auto errorHandler = [](const llvm::Twine &message) {
    llvm::errs() << "error: " << message << "\n";
    return failure();
  };
  if (failed(passPipeline.addToPipeline(pm, errorHandler)))
    return 1;

  if (failed(pm.run(*module)))
    return 1;

  // Print the transformed module.
  module->print(llvm::outs());
  llvm::outs() << "\n";
  return 0;
}
