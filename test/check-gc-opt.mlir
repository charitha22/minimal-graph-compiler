// RUN: gc-opt %s | FileCheck %s

// CHECK:      func.func @add(%arg0: i32, %arg1: i32) -> i32
// CHECK-NEXT:   %0 = arith.addi %arg0, %arg1 : i32
// CHECK-NEXT:   return %0 : i32
// CHECK-NEXT: }

module {
  func.func @add(%arg0: i32, %arg1: i32) -> i32 {
    %0 = arith.addi %arg0, %arg1 : i32
    return %0 : i32
  }
}
