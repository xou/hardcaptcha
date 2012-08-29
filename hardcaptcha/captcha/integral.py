import sympy, random
# and import some commonly used stuff explicitly:
from sympy import sin, cos, integrate, Integral, pi
from mathcaptcha import MathCaptcha, MathChallenge
from response import IntegerResponse, FloatResponse

class SimpleIntegral(MathCaptcha):
    """Simple integral. Choice of boundaries guarantees that result is always an integer. NO WAIT IT DOESNT O FUUU"""
    def getCaptcha(self):
        low_boundaries = (-1, 0, 1)
        lb = random.choice(low_boundaries)
        high_add = (0, 1, 2, 3)
        hb = lb+random.choice(high_add)
        
        x = sympy.Symbol(random.choice(("x", "y", "z", "q", "p")))
        
        fun = random.choice((1, -1))*random.choice((0.5, 1, 2, 3)) * random.choice((1, x)) # TODO x^2
        post = random.choice((-10, -5, 0, 3, 4, 5, 10))
        
        symbolic = Integral(fun, (x, lb, hb)) + post
        result = (integrate(fun, (x, lb, hb)) + post).evalf(3)
        
        return (MathChallenge(symbolic), FloatResponse(result))

class SimpleTrigonometricIntegral(MathCaptcha):
  def __init__(self):
    self.combineMultiple = 2

  def setCombineMultiple(self, amount):
    """Combine this amount of single integral terms"""
    self.combineMultiple = int(amount)

  def generateIntegral(self):
    low_boundaries = (-1, -0.5, 0, 0.5, 1)
    lb = random.choice(low_boundaries)
    high_add = (0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2, 2, 3)
    hb = lb+random.choice(high_add)
    lb = lb*pi
    hb = hb*pi
    fun = random.choice((sin, cos))
    if (random.choice((0,1,2,3,4,5)) == 5):
      tmp = lb
      lb = hb
      hb = lb
    
    x = sympy.Symbol(random.choice(("x", "x", "x", "x", "y", "z", "k")))
    symbolic = Integral(fun(x), (x, lb, hb))
    result = int(integrate(fun(x), (x, lb, hb)).evalf(3))

    return (symbolic, result)

  def getCaptcha(self):
    symbolic = 0;
    result = 0;
    for i in range(0, self.combineMultiple):
      pm = random.choice((1,-1))
      si = self.generateIntegral()
      symbolic += pm*si[0]
      result += pm*si[1]
    return (MathChallenge(symbolic), IntegerResponse(result))
