import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, initialize_app
from flask import Flask, request, render_template, redirect, session, url_for, g, json_available

app = Flask(__name__)
app.secret_key = os.urandom(24)
cred = credentials.Certificate("serviceAccountKey.json")
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')


# firebase_admin.initialize_app(cred)

# db = firestore.client()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        session.pop('user', None)

        username = request.form('username')
        enteredPassword = request.form('password')

        pw = db.collection('users').document(username).get('password')
        if enteredPassword == pw:
            session['user'] = username
            return redirect(url_for('forum'))

    return render_template('index.html')


@app.route('/register')
def register():
    return render_template("index.html")
    Id = request.form("id")
    username = request.form("username")
    password = request.form("password")
    confirmpassword = request.form("confirm_password")
    # image

    if password == confirmpassword:
        data = {'password': password, 'user_name': username}
        db.collection('users').document(Id).set(data)
        return render_template('index.html')


@app.route('/forum')
def forum():
    if g.user:
        return render_template('forum.html', user=session['user'])
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':
    app.run(debug=True)

# db.collection('users').document('').set('')
