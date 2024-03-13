from flask import render_template, session
from app import app


### home ###
@app.route("/")
def customer_tracking():
    #print(session['username'])
    if 'username' in session:
        return render_template('CT_Home.html', username=session['username'])
    else:
        return render_template('CT_Login.html',
                           company_name='Property Appraiser')