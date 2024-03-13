from flask import render_template, request, session, redirect, url_for
from app.ct_login.sql import (user_login_search)
from app import app


### login ###
@app.route("/login", methods=['GET','POST'])
def customer_tracking_login():
    if request.method == 'POST':
        username = request.form.getlist('Username')[0]
        password = request.form.getlist('Password')[0]

        userExists = user_login_search(username, password)

        if userExists == 1:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('CT_Login.html',
                           error='Invalid username or password!')
    else:
        return render_template('CT_Login.html')


### logoff ###
@app.route("/logout")
def customer_tracking_logout():
    session.pop('username', None)
    return redirect(url_for('customer_tracking_login')) #render_template('CT_Login.html')