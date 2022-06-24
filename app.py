# -*- coding: utf-8 -*-

import os
import json

from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

app = Flask(__name__)       # Set static_url_path and static_folder if needed.
app.config.from_object('config')

preview_image_path = {}


class User(UserMixin):
    pass


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
with open('hashed.json') as f:
    user_list = json.load(f)


@login_manager.user_loader
def user_loader(ID):
    if ID not in user_list:
        return
    user = User()
    user.id = ID
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    ID = request.form['user_id']
    if ID in user_list:
        if check_password_hash(user_list[ID], request.form['password']):
            user = User()
            user.id = ID
            login_user(user)
            return redirect(url_for('index'))
    flash('Fail!')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/', methods=['GET'])
@login_required
def index():
    global preview_image_path
    path = request.args.get('path')
    if path is None:
        path = 'static'
    dirs = [f.path for f in os.scandir(path) if f.is_dir()]
    if len(dirs) > 0:
        imgs = [preview_image_path[f] for f in dirs]
    else:
        return redirect(url_for('item', folder=path))
    return render_template('index.html', dirs=dict(zip(dirs, imgs)))


@app.route('/item', methods=['GET'])
@login_required
def item():
    folder = request.args.get('folder')
    imgs = []
    vids = []
    for item in os.scandir(folder):
        if 'mp4' in item.path:
            vids.append(item.path)
        else:
            imgs.append(item.path)
    return render_template('item.html', vids=vids, imgs=imgs)


def get_preview_image_path():
    global preview_image_path
    for path, subdirs, files in os.walk('static'):
        for name in files:
            if '.jpg' in name or '.png' in name:
                fullname = os.path.join(path, name)
                seq = path.split('/')
                while len(seq) > 0:
                    current_path = os.path.join(*seq)
                    if current_path in preview_image_path:
                        break
                    preview_image_path[current_path] = fullname
                    seq.pop()
    for path, subdirs, files in os.walk('static'):
        if path not in preview_image_path:
            preview_image_path[path] = ''
    return


if __name__ == '__main__':
    get_preview_image_path()
    app.logger.info('Listening on http://localhost:8000')
    app.run(host='0.0.0.0', port=8000)
