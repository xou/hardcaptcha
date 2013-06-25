#!/usr/bin/python

import cgitb
cgitb.enable()
import cgi

import sys, os, urlparse
import hardcaptcha
from hardcaptcha.util import lockedshelve
from time import time
captchas = lockedshelve.open("/tmp/hardcaptcha.dev.shelve")

from sympy.printing.latex import latex
try:
  captchaid = int(captchas['counter'])
except KeyError:
  captchaid = 0

def get_captcha(mode='mathjax_latex'):
    global captchas, captchaid
    fields = cgi.FieldStorage()
    if "module" not in fields:
      captcha = hardcaptcha.randomCaptcha()().getCaptcha()
    else:
      captcha = hardcaptcha.selectByString(fields['module'].value)().getCaptcha()
    if not captcha:
      return None
    cid = captchaid
    captchaid += 1
    captchas[str(cid)] = (time(), captcha[1]) # we only need to store the solution
    ret = ""
    if mode=='mathjax_latex':
        ret = "$$"+captcha[0].getLatex()+"$$"
    else:
        raise Exception("Unsupported mode: ", mode)
    ret += "<input type=\"hidden\" name=\"captchaid\" value=\"%d\" />" % cid
    ret += "<br />" + captcha[0].getDesc() + "<br />"
    formatting_help = captcha[1].getFormattingHelp()
    if len(formatting_help):
      ret += "Formatting: " + formatting_help + "<br />"
    return ret

def verify_solution(qvars):
    try:
        userentered = qvars['solution'][0]
        captcha = str(int(qvars['captchaid'][0]))
    except:
        return (False, "Invalid parameters.")

    try:
        captcha_s = captchas[captcha][1]
    except:
        return (False, "Captcha does not exist (anymore)")

    if captcha_s.verify(userentered):
        return (True, "Correct")
    else:
        return (False, "Wrong answer: %s is the correct answer. (or, you've found a bug in this software.)" % captcha_s.getAnswer())

print "Content-type: text/html"
print
print """<html xmlns='http://www.w3.org/1999/xhtml'>
        <head>
        <script type="text/javascript" src="http://bildungsresistenz.de/mathjax/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></head>
        <body>"""
print "<a href=\""+os.environ["SCRIPT_NAME"]+"\">New Captcha</a><br />"

try:
  path = os.environ['REQUEST_URI'].replace(os.environ['SCRIPT_NAME'], "")
except:
  path = "/"

if path=="" or path=="/" or path.startswith("?"):
    print("<h1>HardCaptcha</h1>")
    print("<form method='GET' action='"+os.environ["SCRIPT_NAME"]+"/submit'>")
    captcha = get_captcha()
    if captcha != None:
      print(captcha)
      print("<input type='text' name='solution' /><input type='submit' value='solve'></form>")
    else:
      print "Error: Captcha not found"
    
elif path.startswith('/submit?'):
    qvars = urlparse.parse_qs(path.replace('/submit?', ''))
    s = verify_solution(qvars)
    print "<strong>" + s[1] + "</strong>"
else:
  print "404, sry (path is " + path + ")"

print "<br /><br />"
l = hardcaptcha.getCaptchaList()
for e in l:
  print "<a href='"+os.environ["SCRIPT_NAME"]+"?module="+e+"'>" + e + "</a><br />"
print "<a href='"+os.environ["SCRIPT_NAME"]+"'>Random</a>"
print("<br /><a href='http://github.com/xou/hardcaptcha'>Fork me on Github</a></body></html>")

sys.stdout.flush()
removefrom = time() - 60*60*2

# TODO this is slow, replace with SQL or something more smart
keys = captchas.keys()
for k in keys:
  if k == 'counter':
    continue
  if captchas[k][0] < removefrom:
    del captchas[k]

#print captchas
captchas['counter'] = captchaid
captchas.close()
