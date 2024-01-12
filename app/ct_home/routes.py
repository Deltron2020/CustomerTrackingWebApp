from flask import render_template
from app import app


### home ###
@app.route("/")
def customer_tracking():
    return render_template('CT_Home.html',
                           company_name='Property Appraiser')