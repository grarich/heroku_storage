import os
import random
import string

from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

# URLの最後の"/"がない場合のエラーを回避
app.url_map.strict_slashes = False

files = []
os.mkdir('./aszifynvilsayv')

class File:
    def __init__(self, filename, passwd):
        self.filename = filename
        self.passwd = passwd


# 最初に開くページ
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# ファイルをPOSTした時の処理
@app.route('/', methods=['POST'])
def save_file():
    global files
    filename = request.files.get('file').filename
    file = request.files.get('file')
    file.save(f'./aszifynvilsayv/{filename}')
    passwd = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    saved = File(filename, passwd)
    files.append(saved)

    return render_template(
        'index.html',
        flag=True,
        file=saved.filename,
        passwd=saved.passwd
    )
                 
@app.route('/<passwd>')
def view_file(passwd):
    global files
    send_file = [f for f in files if f.passwd == passwd]
    if not send_file:
        return render_template(
            'index.html',
            message='パスが違う！！'
        )
    return send_file(f'./aszifynvilsayv/{send_file[0].filename}')

# 404
@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404

# 500
@app.errorhandler(500)
def server_error(_):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'))
