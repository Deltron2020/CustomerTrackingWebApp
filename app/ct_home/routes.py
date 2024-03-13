from flask import render_template, session, redirect, url_for
from app import app


### home ###
@app.route("/")
def customer_tracking():
    #print(session['username'])
    if 'username' in session:
        return render_template('CT_Home.html')
    else:
        return redirect(url_for('customer_tracking_login'))