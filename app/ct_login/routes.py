from flask import render_template, request, session, redirect, url_for
from app.ct_login.sql import (user_login_search, user_dept_check)
from app import app


### login ###
@app.route("/login", methods=['GET','POST'])
def customer_tracking_login():
    try:
        if request.method == 'POST':
            username = request.form.get('Username')
            password = request.form.get('Password')

            userExists = user_login_search(username, password)

            if userExists == 1:
                session['username'] = username.lower()
                session['admin'] = user_dept_check(username,1) # 1=IT
                return redirect('/')
            else:
                return render_template('CT_Login.html',
                               error='Invalid username or password!')
        else:
            return render_template('CT_Login.html')
    except Exception as e:
        return render_template('CT_Error.html', error=e)


### logoff ###
@app.route("/logout")
def customer_tracking_logout():
    try:
        session.pop('username', None)
        return redirect(url_for('customer_tracking_login')) #render_template('CT_Login.html')
    except Exception as e:
        return render_template('CT_Error.html', error=e)