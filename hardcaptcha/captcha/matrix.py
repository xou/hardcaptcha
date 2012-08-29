import sympy, random
# and import some commonly used stuff explicitly:
#from sympy import sin, cos, integrate, Integral, pi
from sympy.matrices import matrices
from mathcaptcha import MathCaptcha, VecMulChallenge, DetMatrixChallenge
from response import IntegerResponse, FloatResponse, VectorResponse


class SimpleVectorMultiplication(MathCaptcha):
    """Multiply two vectors"""
    def __init__(self, dim=3):
        self.dim = dim

    def getCaptcha(self):
        vecA = matrices.randMatrix(self.dim, 1, min=0, max=5)
        vecB = matrices.randMatrix(1, self.dim, min=0, max=5)

        symbolic = vecA * vecB
        crnum = random.choice(range(0, self.dim))
        
        result = symbolic[:,crnum]
        symbolic[:,crnum] = sympy.symbols(['a','b','c'])
        
        return (VecMulChallenge(vecA, vecB, symbolic, desc="Enter the missing column"),
                VectorResponse(result))



class Determinant(MathCaptcha):
    """Calculate determinant of a matrix"""
    def __init__(self, dim=2):
        self.dim = dim

    def getCaptcha(self):
        matrix = matrices.randMatrix(self.dim, self.dim, min=-3, max=3)
        result = matrix.det()
        return (DetMatrixChallenge(matrix), IntegerResponse(result))
