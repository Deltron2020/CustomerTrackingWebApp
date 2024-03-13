from flask import render_template, request, session, redirect, url_for
from app.ct_create_ticket.sql import (load_accounts_from_db, populate_ticket_account_data, add_ticket_to_db)
from app import app


### locate account & create ticket ###
@app.route("/create", methods=['GET'])
def customer_tracking_create():
    if 'username' in session:
        data = request.args     # data returned from inputs (4 possible fields)
        account = {}    # dictionary to hold entered data
        for i in data:
            if (len(data[i])) > 0:
                value = {i: data[i]}
                account.update(value)
                #print(account)
                break

        results = []
        for v in account:
            results = load_accounts_from_db(v, account[v])

        return render_template('CT_Create.html',
                               account_data=results)
    else:
        return redirect(url_for('customer_tracking_login'))


### create ticket w account data ###
@app.route("/ticket/<account>")
def create_ticket_for_account(account):
    if 'username' in session:
        account_data = populate_ticket_account_data(account)
        if not account_data:
            return render_template('CT_Ticket.html', create_user=session['username'])
        #print(account_data)
        else:
            return render_template('CT_Ticket.html',
                                   account=account_data,
                                   create_user=session['username'])
    else:
        return redirect(url_for('customer_tracking_login'))


### create blank ticket ###
@app.route("/ticket")
def create_ticket():
    if 'username' in session:
        return render_template('CT_Ticket.html',
                               account=[],
                               create_user=session['username'])
    else:
        return redirect(url_for('customer_tracking_login'))


### submit new ticket data into table ###
@app.route("/ticket/submitted", methods=['POST'])
def submit_ticket():
    if 'username' in session:
        data = request.form
        add_ticket_to_db(data)
        return render_template('CT_Submitted.html')
    else:
        return redirect(url_for('customer_tracking_login'))
