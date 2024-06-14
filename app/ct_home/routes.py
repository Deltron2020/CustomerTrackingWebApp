from flask import render_template, session, redirect, url_for
from app import app


### home ###
@app.route("/")
def customer_tracking():
    try:
        if 'username' in session:
            return render_template('CT_Home.html',isAdmin=session['admin'])
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)