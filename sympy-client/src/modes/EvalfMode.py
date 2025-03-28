from modes.EvalModeBase import EvaluateMessage, eval_mode_base, try_assign

from ModeResponse import ModeResponse
from grammar.SympyParser import SympyParser

from sympy import *

## Tries to evaluate the last equality of an latex equation.
async def evalf_handler(message: EvaluateMessage, response: ModeResponse, parser: SympyParser):
    def evaluate(sympy_expr):
        sympy_expr = try_assign(sympy_expr.evalf(), sympy_expr)
        
        return sympy_expr
           
    return await eval_mode_base(message, response, parser, evaluate)
