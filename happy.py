# -*- coding: utf-8 -*-

# @Time     : 2018/4/6
# @Author   : WangL
# @File     : happy.py

from flask import Flask, url_for, request, render_template, redirect
from data_factory import DataFactory

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<user_name>')
def show_user_profile(user_name):
    return 'User name is : {}'.format(user_name)


@app.route('/post/<int:id>')
def show_post(post_id):
    return 'post id is : {}'.format(post_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['query']
        data_info = DataFactory()
        data_info.query_img(name)
        return redirect(url_for('show_user_profile', user_name=name))
    else:
        return render_template('m.html')

if __name__ == '__main__':
    app.run(debug=True)
