from flask import *
import os

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def register():
    print(request.form.get("username"))
    print(request.form.get("password"))
    return "注册成功"


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join("uploads", os.path.basename(file.filename)))
        return "文件上传成功"

'''
当该文件被当作导入的时候 ，就不会被执行
'''
if __name__ == '__main__':
    app.run()
