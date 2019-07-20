'''
抓取需要身份验证的页面

'''

from flask import *
import base64

app = Flask(__name__)


def hasAuth(auth, resp):
    if auth is None or auth.strip() == "":
        resp.status_code = 401
        resp.headers['WWW-Authenticate'] = 'Basic realm="localhost"'
        return False
    return True


#
@app.route("/")
def index():
    response = app.make_response("username or password error")
    print(request.headers)
    auth = request.headers.get("Authorization")
    print('Authorization:', auth)
    if hasAuth(auth, response):
        auth = str(base64.b64decode(auth.split(' ')[1]), 'utf-8')
        print(auth)
        values = auth.split(":")
        username = values[0]
        password = values[1]
        if username == 'lqd' and password == '123456':
            response.status_code = 200
            return "success"
        else:
            response.status_code = 401
            return "fail"
    return response


if __name__ == '__main__':
    app.run()
