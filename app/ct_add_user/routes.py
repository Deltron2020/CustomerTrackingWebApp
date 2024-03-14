from flask import render_template, request, session, redirect, url_for
from app.ct_add_user.sql import (add_newuser_to_db)
from app import app

### add a new user ###
@app.route("/adduser")
def add_new_user():
    if 'username' in session and session['admin'] == 1:
        return render_template('CT_AddUser.html')
    else:
        return redirect(url_for('customer_tracking_login'))


### submit new user to database ###
@app.route("/adduser/submitted", methods=['POST'])
def submit_new_user():
    if 'username' in session and session['admin'] == 1:
        data = request.form
        add_newuser_to_db(data, session['username'])

        return render_template('CT_Submitted.html',
                               newUser=data['UserName'])
    else:
        return redirect(url_for('customer_tracking_login'))