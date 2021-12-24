# -*- coding: utf-8 -*-

import os
import json

from flask import Flask, request, render_template, url_for, redirect, flash
from flask import send_file, abort
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.security import check_password_hash

app = Flask(__name__)       # Set static_url_path and static_folder if needed.
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

with open('static/hashed.json') as f:
    user_list = json.load(f)

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

# ------------------------------------------------------------ #

@app.route('/', methods=['GET'])
@login_required
def index():
    dirs = [x for x in os.listdir('static') if os.path.isdir(f'static/{x}')]
    return render_template('index.html', dirs=dirs)

@app.route('/item/<path:sd>', methods=['GET'])
@login_required
def item(sd):
    images = []
    videos = []
    for filename in os.listdir('static/' + sd):
        if 'mp4' in filename:
            videos.append(filename)
        else:
            images.append(filename)
    return render_template('item.html', sd=sd, videos=videos, images=images)

@app.route('/image/<path:sd>', methods=['GET'])
@login_required
def get_image(sd):
    if os.path.isfile(f'static/{sd}/{sd}-001.jpg'):
        return send_file(f'static/{sd}/{sd}-001.jpg', mimetype='image/jpeg')
    if os.path.isfile(f'static/{sd}/{sd}-001.png'):
        return send_file(f'static/{sd}/{sd}-001.png', mimetype='image/png')  
    return abort(404)

if __name__ == '__main__':
    app.logger.info('Listening on http://localhost:8000')
    app.run(host='0.0.0.0', port=8000)
