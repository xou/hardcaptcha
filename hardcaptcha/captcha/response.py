import re

class Response:
    def verify(self, string):
        raise Exception("Not implemented: checkAnswer")

    def getAnswer(self):
        """Return a representation of the solution."""
        raise Exception("Not implemented: getAnswer")

    def getFormattingHelp(self):
        return ""

class IntegerResponse(Response):
    def __init__(self, result):
        self.res = int(result)
        
    def verify(self, answer):
        try:
            answer = int(answer)
        except ValueError:
            return False
        
        return answer == self.res
    
    def getAnswer(self):
        return str(self.res)


class VectorResponse(Response):
  def __init__(self, result, formatting="Enter the values comma-seperated: a, b, ..., n"):
    self.result = result
    self.formatting = formatting

  def verify(self, answer):
    length = 0
    # this is a workaround, since pre 0.7 versions of Matrix do not support len()
    try:
      length = len(self.result)
    except:
      for m in self.result:
        length += 1

    try:
      # handle [a,b,c] or (a,b,c) notation
      if ((answer.startswith('[') and answer.endswith(']'))
         or (answer.startswith('(') and answer.endswith(')'))):
        answer = answer[1:-1]

      answer = re.split("[ ,]+", str(answer))
      for k in range(0, length):
        if (int(answer[k].strip()) != int(self.result[k])):
          return False
    except:
      raise
      return False
    return True

  def getAnswer(self):
    return ", ".join([str(int(x)) for x in self.result])

  def getFormattingHelp(self):
    return self.formatting


class FloatResponse(Response):
    def __init__(self, result, prec=3):
        """precision-paramter defines how many digits after the decimal point need to be correct."""
        self.res = result
        self.prec = 10**-prec
    
    def verify(self, answer):
        try:
            answer = float(answer)
        except ValueError:
            return False
        
        return abs(answer-self.res) < self.prec
    
    def getAnswer(self):
        return "%.3f" % self.res

