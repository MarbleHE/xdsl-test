from pathlib import Path
from xdsl import *
from xdsl.ir import *
from xdsl.irdl import *
from xdsl.dialects.std import *
from xdsl.dialects.arith import *
from xdsl.dialects.builtin import *
#TODO: Does xDSL support tensor?
from xdsl.parser import *
from xdsl.printer import *
from xdsl.util import *

from dialects.poly import *
from dialects.fhe import *

# MLContext, containing information about the registered dialects
context = MLContext()

# Some useful dialects
std = Std(context)
arith = Arith(context)
builtin = Builtin(context)
fhe = FHE(context)
poly = Poly(context)

# Printer used to pretty-print MLIR data structures
printer = Printer()

# Simple hardcoded test, doesn't work for now because we didn't define custom assembly
test_program = Path('tests/multiply.mlir').read_text()
parser = Parser(context, test_program)
module = parser.parse_op()
module.verify()
