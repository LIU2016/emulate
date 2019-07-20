'''

cookie

'''

from flask import *

app = Flask(__name__)


@app.route("/readCookie")
def readCookie():
    print(request.cookies)
    print(request.cookies.get('MyCookie'))
    return "readCookie success!"


@app.route("/setCookie")
def setCookie():
    response = app.make_response('write cookie')
    response.set_cookie("id", value="000000")
    return response


if __name__ == '__main__':
    app.run()
