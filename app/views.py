from app import app
from flask import render_template, redirect, url_for
from flask_login import logout_user, current_user, login_required


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    return render_template('authorization.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template(
        'index.html',
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        friends=current_user.friends
    )


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))
