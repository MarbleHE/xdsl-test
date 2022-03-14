// RUN: fhe-compiler --fhe2poly --cse --canonicalize < %s | FileCheck %s
%0 = fhe.load_ctxt {file = "a.ctxt", parms = "foo.parms"} : !fhe.ctxt<2x!poly.poly<4096, true, 2, "foo.parms">>
%1 = fhe.load_ctxt {file = "b.ctxt", parms = "foo.parms"} : !fhe.ctxt<2x!poly.poly<4096, true, 2, "foo.parms">>
%2 = fhe.multiply(%0, %1) : (!fhe.ctxt<2x!poly.poly<4096, true, 2, "foo.parms">>, !fhe.ctxt<2x!poly.poly<4096, true, 2, "foo.parms">>) -> !fhe.ctxt<3x!poly.poly<4096, true, 2, "foo.parms">>
fhe.sink(%2) : (!fhe.ctxt<3x!poly.poly<4096, true, 2, "foo.parms">>)

// CHECK: module  {
// CHECK:   %0 = fhe.load_ctxt {file = "a.ctxt", parms = "foo.parms"} : !fhe.ctxt<2 x !poly.poly<4096, true, 2, "foo.parms">>
// CHECK:   %1 = fhe.load_ctxt {file = "b.ctxt", parms = "foo.parms"} : !fhe.ctxt<2 x !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %2 = poly.to_poly(%0) {i = 0 : index} : (!fhe.ctxt<2 x !poly.poly<4096, true, 2, "foo.parms">>) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %3 = poly.to_poly(%1) {i = 0 : index} : (!fhe.ctxt<2 x !poly.poly<4096, true, 2, "foo.parms">>) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %4 = poly.to_poly(%0) {i = 1 : index} : (!fhe.ctxt<2 x !poly.poly<4096, true, 2, "foo.parms">>) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %5 = poly.to_poly(%1) {i = 1 : index} : (!fhe.ctxt<2 x !poly.poly<4096, true, 2, "foo.parms">>) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %6 = poly.multiply(%2, %3) : (!poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %7 = poly.multiply(%4, %3) : (!poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %8 = poly.multiply_accumulate(%2, %5, %7) : (!poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %9 = poly.multiply(%4, %5) : (!poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">) -> !poly.poly<4096, true, 2, "foo.parms">
// CHECK:   %10 = poly.to_ctxt(%6, %8, %9) : (!poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">, !poly.poly<4096, true, 2, "foo.parms">) -> !fhe.ctxt<3 x !poly.poly<4096, true, 2, "foo.parms">>
// CHECK:   fhe.sink(%10) : (!fhe.ctxt<3 x !poly.poly<4096, true, 2, "foo.parms">>)
// CHECK: }
