from tests.TestResponse import TestResponse
from modes.EvaluateMode import evaluateMode
import asyncio

from sympy import *


## Tests the evaluate mode.
class TestEvaluate:
    
    def test_simple_evaluate(self):
        response = TestResponse()
        asyncio.run(evaluateMode({"expression": "1+1", "environment": {}}, response))
        assert response.hasResult()
        
        result = response.getResult()
            
        with evaluate(False):
            assert result['result'] == Eq(2, 2)
            
    def test_escaped_spaces(self):
        response = TestResponse()
        asyncio.run(evaluateMode({"expression": r"1\ + \ 1", "environment": {}}, response))
        assert response.hasResult()
        
        result = response.getResult()
            
        with evaluate(False):
            assert result['result'] == Eq(2, 2)
        
        
    def test_matrix_single_line(self):
        response = TestResponse()
        asyncio.run(evaluateMode({"expression": r"2 \cdot \begin{bmatrix} 1 \\ 1 \end{bmatrix}", "environment": {}}, response))
        assert response.hasResult()
        
        result = response.getResult()

        assert result['result'].rhs == 2 * Matrix([[1], [1]])
        
                
    def test_matrix_multi_line(self):
        response = TestResponse()
        asyncio.run(evaluateMode({"expression": r"""
        2
        \cdot 
        \begin{bmatrix} 
        1 \\ 1
        \end{bmatrix}
        """, "environment": {}}, response))
        
        assert response.hasResult()
        
        result = response.getResult()

        assert result['result'].rhs == 2 * Matrix([[1], [1]])
        
    def test_matrix_normal(self):
        response = TestResponse()
        asyncio.run(evaluateMode({"expression": r"""
        \Vert
        \begin{bmatrix}
        20 \\
        30 \\
        40 \\
        50
        \end{bmatrix}
        \Vert
        """, "environment": {}}, response))
        
        assert response.hasResult()
        
        result = response.getResult()

        assert result['result'].rhs == sqrt(20**2 + 30**2 + 40**2 + 50**2)
        
    def test_matrix_inner_prodcut(self):
        response = TestResponse()
        asyncio.run(evaluateMode({"expression": r"""
        \langle 
        \begin{bmatrix}
        1 \\
        2
        \end{bmatrix}
        |
        \begin{bmatrix}
        2 \\
        4
        \end{bmatrix}
        \rangle
        """, "environment": {}}, response))
        
        assert response.hasResult()
        
        result = response.getResult()

        assert result['result'].rhs == 1 * 2 + 2 * 4