import hardcaptcha
from sympy.printing.mathml import mathml
from sympy.printing.latex import latex
import BaseHTTPServer
import sys
import urlparse

ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

port = 8888
if sys.argv[1:]:
    port = int(sys.argv[1])

captchaid = 0
captchas = {}
server_addr = ('', port)

def get_captcha(captcha=None, mode='mathjax_latex'):
    global captchas, captchaid
    if captcha == None:
        captcha = hardcaptcha.randomCaptcha()().getCaptcha()
    cid = captchaid
    captchaid += 1
    captchas[cid] = captcha[1] # we only need to store the solution
    ret = ""
    if mode=='mathjax_latex':
        ret = "$$"+captcha[0].getLatex()+"$$"
    else:
        raise Exception("Unsupported mode" + mode)
    ret += "<input type=\"hidden\" name=\"captchaid\" value=\"%d\" />" % cid
    return ret

class HCServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def verify_solution(self, qvars):
        try:
            userentered = qvars['solution'][0]
            captcha = int(qvars['captchaid'][0])
        except:
            self.wfile.write("Invalid parameters.")
            return False
        
        try:
            captcha_s = captchas[captcha]
        except:
            self.wfile.write("Captcha does not exist (anymore)")
            return False
        
        if captcha_s.verify(userentered):
            self.wfile.write("Answer correct.")
            return True
        else:
            self.wfile.write("Wrong answer: %s is the correct answer. (or, you've found a bug in this software.)" % captcha_s.getAnswer())
            return False
        
    def do_GET(self):
        global captchas
        s = self
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("""<html xmlns='http://www.w3.org/1999/xhtml'>
        <head>
        <script type="text/javascript" src="http://bildungsresistenz.de/mathjax/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script></head>
        <body><a href="/">New Captcha</a><br />""")
        
        qvars = urlparse.parse_qs(s.path.replace('/?', ''))
        if s.path.startswith('/submit?'):
            qvars = urlparse.parse_qs(s.path.replace('/submit?', ''))
            self.verify_solution(qvars)

        s.wfile.write("<form method='GET' action='/submit'>")
  
        if 'module' not in qvars:
            s.wfile.write(get_captcha())
        else:
            captcha = hardcaptcha.selectByString(qvars['module'][0])().getCaptcha()
            s.wfile.write(get_captcha(captcha))
            s.wfile.write("<input type='hidden' name='module' value='" + qvars['module'][0] + "' />")
            s.wfile.write("<input type='text' name='solution' /></form>")
        s.wfile.write("<br /><br />")

        l = hardcaptcha.getCaptchaList()
        for e in l:
          s.wfile.write("<a href='/?module="+e+"'>" + e + "</a><br />")
        s.wfile.write("<a href='/'>Random</a>")
        s.wfile.write("<br /><a href='http://github.com/xou/hardcaptcha'>Fork me on Github</a></body></html>")
        s.wfile.write("</body></html>")
        
httpd = BaseHTTPServer.HTTPServer(server_addr, HCServerHandler)
httpd.serve_forever()
