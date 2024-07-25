from flask import render_template, request, session, redirect, url_for
from app import app


@app.route("/dashboard")
def populate_dashboard():
    try:
        if 'username' in session and session['admin'] == 1:
            return render_template('CT_Dashboard.html')
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)
