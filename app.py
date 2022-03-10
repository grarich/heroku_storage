import os
import random
import string

from flask import Flask, abort, render_template, request, redirect, send_from_directory

app = Flask(__name__)

# URLの最後の"/"がない場合のエラーを回避
app.url_map.strict_slashes = False

files = []

warn_ip = []
warn_ip_2 = []
banned_ip = []


class File:
    def __init__(self, filename, passwd):
        self.filename = filename
        self.passwd = passwd


# 最初に開くページ
@app.route('/', methods=['GET'])
def index():
    print(banned_ip)
    if request.remote_addr in banned_ip:
        return abort(403)
    return render_template('index.html')


# ファイルをPOSTした時の処理
@app.route('/', methods=['POST'])
def save_file():
    global files
    filename = request.files.get('file').filename
    file = request.files.get('file')
    passwd = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    os.mkdir(f'./{passwd}')
    file.save(f'./{passwd}/{filename}')
    saved = File(filename, passwd)
    files.append(saved)

    return render_template(
        'index.html',
        flag=True,
        file=saved.filename,
        passwd=saved.passwd
    )


def check_ip(ip_addr):
    if ip_addr in banned_ip:
        return
    if ip_addr in warn_ip_2:
        banned_ip.append(ip_addr)
        warn_ip_2.remove(ip_addr)
        return
    if ip_addr in warn_ip:
        warn_ip_2.append(ip_addr)
        warn_ip.remove(ip_addr)
        return


@app.route('/<passwd>')
def view_file(passwd):
    global files
    print(banned_ip)
    if request.remote_addr in banned_ip:
        return abort(403)
    send_files = [f for f in files if f.passwd == passwd]
    if not send_files:
        check_ip(request.remote_addr)
        return render_template(
            'index.html',
            message='パスが違う！！'
        )
    path = send_files[0].filename
    return send_from_directory(f'./{passwd}', path, as_attachment=True, attachment_filename=send_files[0].filename)

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
