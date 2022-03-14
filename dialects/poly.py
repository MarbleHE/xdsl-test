from __future__ import annotations
from attr import attributes
from xdsl.dialects.builtin import *

from dialects.fhe import CiphertextType


@dataclass
class Poly:
    ctx: MLContext

    def __post_init__(self):
        self.ctx.register_op(ToPoly)
        self.ctx.register_op(ToCtxt)
        self.ctx.register_op(Multiply)
        self.ctx.register_op(MultiplyAccumulate)


@irdl_attr_definition
class PolynomialType(ParametrizedAttribute):
    name = "poly"

    # 4096, true, 2, "foo.parms"
    degree = ParameterDef(IntegerAttr)
    isNTT = ParameterDef(IntegerAttr)  #TODO: How to make this a boolean?
    numRNS = ParameterDef(IntegerAttr)
    params = ParameterDef(StringAttr)

    def get_size(self) -> int:
        return self.shape

    def get_element_type(self) -> AnyAttr:
        return self.element_type

    @staticmethod
    @builder
    def from_type_and_size(degree: int, isNTT: bool, numRNS: int,
                           params: str) -> PolynomialType:
        return PolynomialType([
            IntegerAttr.build(degree),
            IntegerAttr.build(isNTT),
            IntegerAttr.build(numRNS),
            StringAttr.from_str(params)
        ])


@irdl_op_definition
class Multiply(Operation):
    name: str = "poly.multiply"
    x = OperandDef(PolynomialType)
    y = OperandDef(PolynomialType)
    output = ResultDef(PolynomialType)

    def verify_(self) -> None:
        if self.x.typ != self.y.typ or self.x.typ != self.output.typ:
            raise Exception("expect all input and output types to be equal")

    @staticmethod
    def get(x: Union[Operation, SSAValue], y: Union[Operation,
                                                    SSAValue]) -> Multiply:
        return Multiply.build(operands=[x, y], result_types=[x.typ])


@irdl_op_definition
class MultiplyAccumulate(Operation):
    name: str = "poly.multiply_accumulate"
    x = OperandDef(PolynomialType)
    y = OperandDef(PolynomialType)
    output = ResultDef(PolynomialType)

    def verify_(self) -> None:
        if self.x.typ != self.y.typ or self.x.typ != self.output.typ:
            raise Exception("expect all input and output types to be equal")

    @staticmethod
    def get(x: Union[Operation, SSAValue],
            y: Union[Operation, SSAValue]) -> MultiplyAccumulate:
        return MultiplyAccumulate.build(operands=[x, y], result_types=[x.typ])


@irdl_op_definition
class ToPoly(Operation):
    name: str = "poly.to_poly"
    x = OperandDef(
        AnyAttr
    )  #TODO: How to constrain this to Ciphertext without circular dependencies?
    i = AttributeDef(IntegerAttr)
    output = ResultDef(PolynomialType)

    @staticmethod
    def get(x: Union[Operation, SSAValue], i: int) -> ToPoly:
        return ToPoly.build(operands=[x],
                            attributes={"i": IntegerAttr.build(i)},
                            result_types=[x.typ])


@irdl_op_definition
class ToCtxt(Operation):
    name: str = "poly.to_ctxt"
    x = VarOperandDef(PolynomialType)
    output = ResultDef(CiphertextType)

    # TODO: How to build return type here?

    #TODO: Does something need to change here because x is variadic?
    @staticmethod
    def get(x: Union[Operation, SSAValue]) -> ToCtxt:
        return ToCtxt.build(operands=[x], result_types=[])
