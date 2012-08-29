from sympy.printing.latex import latex
import re

class MathCaptcha:
  def getCaptcha(self):
    return None


class Challenge:
  """Base class for a challenge, i.e. a formula.
     Currently, the only class deriving from this is LaTeXChallenge, which uses getLatex for latex output.
     However, it might be possible to include other types of captchas and output using, for example, a
     getHTML method, where applicable.
     """

  def getDesc(self):
    """Return a desciption of how to solve this captcha. ("Find the roots of the given equation")"""
    return ""

class MathChallenge(Challenge):
  def __init__(self, expr):
    self.expr = expr

  def fixLatex(self, string):
    """Workaround for older sympy versions, where the LaTeX-printer ignores the "mode" setting"""
    if string.startswith("$") and string.endswith("$"):
      return string[1:-1]
    return string

  def getLatex(self):
    fl = lambda x: self.fixLatex(latex(x, mode="plain"))
    return fl(self.expr)

class VecMulChallenge(MathChallenge):
  """Starting with SymPy 0.7.2, SymPy supports ImmutableMatrix, which would allow
     direct display of matrix equations using MathChallenge. However, at the time of writing,
     0.7.1 is still current, so this is a workaround."""
  def __init__(self, vA, vB, M, desc="solve"):
    self.vA = vA
    self.vB = vB
    self.M  = M
    self.desc = desc

  def getLatex(self):
    fl = lambda x: self.fixLatex(latex(x, mode="plain"))
    return fl(self.vA) + "*" + fl(self.vB) + "=" + fl(self.M)

  def getDesc(self):
    return self.desc

class DetMatrixChallenge(MathChallenge):
  def __init__(self, M):
    self.M = M

  def getLatex(self):
    fl = lambda x: self.fixLatex(latex(x, mode="plain"))
    return  "det" + fl(self.M)

  def getDesc(self):
    return "Calculate determinant of the given matrix"
