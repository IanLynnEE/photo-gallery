# -*- coding: utf-8 -*-

import os
import json

from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash


# ==================== Global Variables ==================== #
app = Flask(__name__)       # Set static_url_path and static_folder if needed.
app.config.from_object('config')

thumbnail_paths = {}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
with open('hashed.json') as f:
    user_list = json.load(f)


# ====================      Login       ==================== #
class User(UserMixin):
    pass


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


# ====================    Main Page     ==================== #
@app.route('/', methods=['GET'])
@login_required
def index():
    global thumbnail_paths

    # Get the path from the request in order to display things under the path.
    path = 'static' if (path := request.args.get('path')) is None else path

    # Get a list of subdirectories under the current path.
    # If there is no subdirectory, redirect to item page.
    dirs = [f.path for f in os.scandir(path) if f.is_dir()]
    if len(dirs) == 0:
        return redirect(url_for('item', folder=path))

    # Get the thumbnail for each subdirectory.
    imgs = [thumbnail_paths[f] for f in dirs]
    return render_template('index.html', dirs=dict(zip(dirs, imgs)))


# ====================    Item Page     ==================== #
@app.route('/item', methods=['GET'])
@login_required
def item():
    folder = request.args.get('folder')
    vids = [f.path for f in os.scandir(folder) if f.name.endswith('.mp4')]
    imgs = [f.path for f in os.scandir(folder) if is_image(f.name)]
    return render_template('item.html', vids=vids, imgs=imgs)


# ====================      Utils       ==================== #
def is_image(filename: str) -> bool:
    img_extensions = ['.jpg', '.png', '.gif', '.bmp', '.jpeg', '.webp', 'avif']
    for e in img_extensions:
        if filename.endswith(e):
            return True
        if filename.endswith(e.upper()):
            return True
    return False


# IIFE
@lambda _: _()
def get_thumbnails():
    global thumbnail_paths
    # Get all images in the static folder.
    for root, dirs, files in os.walk('static'):
        for file in files:
            if is_image(file):
                filename = os.path.join(root, file)
                if os.path.getsize(filename) > 1024:
                    thumbnail_paths[filename] = filename
    # Set the thumbnail for each subdirectory.
    for key, value in sorted(thumbnail_paths.items()):
        path_seq = key.split(os.sep)
        path_seq.pop()
        while len(path_seq) > 0:
            path = os.path.join(*path_seq)
            # If a path has been set, the consiquent paths must have been set.
            if path in thumbnail_paths:
                break
            thumbnail_paths[path] = value
            path_seq.pop()
    # Avoid KeyError.
    for root, dirs, files in os.walk('static'):
        if root not in thumbnail_paths:
            thumbnail_paths[root] = ''
    return


if __name__ == '__main__':
    app.logger.info('Listening on http://localhost:8000')
    app.run(host='0.0.0.0', port=8000)
