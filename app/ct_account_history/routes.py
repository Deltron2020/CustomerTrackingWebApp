from flask import render_template, request, session, redirect, url_for
from app.ct_account_history.sql import (load_account_ticket_history_from_db, load_account_from_db)
from app import app


### locate account (account search) ###
@app.route("/account/<accountNumber>")
def account_ticket_history(accountNumber):
    try:
        if 'username' in session:
            ticketHistory = load_account_ticket_history_from_db(accountNumber)
            account = load_account_from_db(accountNumber)

            return render_template('CT_AccountHistory.html', ticket_history=ticketHistory, account_data=account)
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)