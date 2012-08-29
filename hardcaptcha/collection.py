import random
import captcha

captchas = []
captchas.append(captcha.integral.SimpleTrigonometricIntegral)
captchas.append(captcha.integral.SimpleIntegral)
captchas.append(captcha.matrix.SimpleVectorMultiplication)
captchas.append(captcha.matrix.Determinant)


def randomCaptcha():
  return random.choice(captchas)

def getCaptchaList():
  ret = []
  for c in captchas:
    ret.append(c.__module__ + "." + c.__name__)
  return ret

def selectByString(s):
  for c in captchas:
    if c.__module__ + "." + c.__name__ == s:
      return c
