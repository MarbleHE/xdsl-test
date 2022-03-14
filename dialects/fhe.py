from __future__ import annotations
from attr import attributes
from xdsl.dialects.builtin import *


@dataclass
class FHE:
    ctx: MLContext

    def __post_init__(self):
        self.ctx.register_op(LoadCiphertext)
        self.ctx.register_op(Sink)
        self.ctx.register_op(Multiply)


@irdl_attr_definition
class CiphertextType(ParametrizedAttribute):
    name = "ctxt"

    shape = ParameterDef(IntegerAttr)
    element_type = ParameterDef(
        AnyAttr()
    )  # TODO: How to get this to refer to PolynomialType without circular dependency?

    def get_size(self) -> int:
        return self.shape

    def get_element_type(self) -> AnyAttr:
        return self.element_type

    @staticmethod
    @builder
    def from_type_and_attr(referenced_type: Attribute,
                           size: IntegerAttr) -> CiphertextType:
        return CiphertextType([size, referenced_type])

    @staticmethod
    @builder
    def from_type_and_size(referenced_type: Attribute,
                           size: int) -> CiphertextType:
        return CiphertextType.from_type_and_attr(referenced_type,
                                                 IntegerAttr.build(size))


@irdl_op_definition
class Multiply(Operation):
    name: str = "fhe.multiply"
    x = OperandDef(CiphertextType)
    y = OperandDef(CiphertextType)
    output = ResultDef(CiphertextType)

    def verify_(self) -> None:
        if self.x.typ != self.y.typ:
            raise Exception("expect input types to be equal")
        # TODO: How to check if x has size == 2?

    @staticmethod
    def get(x: Union[Operation, SSAValue], y: Union[Operation,
                                                    SSAValue]) -> Multiply:
        return Multiply.build(operands=[x, y],
                              result_types=[
                                  CiphertextType.from_type_and_size(
                                      x.get_element_type(), 3)
                              ])


@irdl_op_definition
class LoadCiphertext(Operation):
    name: str = "fhe.load_ctxt"
    input_file = AttributeDef(StringAttr)
    output = ResultDef(CiphertextType)

    @staticmethod
    def get(file_name: str, typ: CiphertextType) -> LoadCiphertext:
        return Multiply.build(
            operands=[],
            attributes={"input_file": StringAttr.from_str(file_name)},
            result_types=[typ])


@irdl_op_definition
class Sink(Operation):
    name: str = "fhe.sink"
    input = OperandDef(CiphertextType)

    @staticmethod
    def get(x: Union[Operation, SSAValue]) -> Sink:
        return Sink.build(operands=[x])
