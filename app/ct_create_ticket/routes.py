from flask import render_template, request, session, redirect, url_for
from app.ct_create_ticket.sql import (load_accounts_from_db, populate_ticket_account_data, add_ticket_to_db, account_ticket_search)
from app import app


### locate account (account search) ###
@app.route("/create", methods=['GET'])
def customer_tracking_create():
    if 'username' in session:
        data = request.args     # data returned from inputs (4 possible fields)
        account = {}    # dictionary to hold entered data
        for i in data:
            if (len(data[i])) > 0:
                value = {i: data[i]}
                account.update(value)

        query_filter = ''
        for e, field in enumerate(account):
            if e == 0:
                query_filter += (f"WHERE {field} LIKE '%{account[field]}%'")
            elif e >= 1:
                query_filter += (f" AND {field} LIKE '%{account[field]}%'")

        if not query_filter:
            results = []
            return render_template('CT_Create.html',
                               account_data=results)
        else:
            results = load_accounts_from_db(query_filter)
            return render_template('CT_Create.html',
                               account_data=results)
    else:
        return redirect(url_for('customer_tracking_login'))


### create ticket w account data ###
@app.route("/ticket/<account>")
def create_ticket_for_account(account):
    if 'username' in session:
        account_data = populate_ticket_account_data(account)
        ticket_exists = account_ticket_search(account)  # see if ticket already exists, if so prompt the user to either load the ticket or continue creating a new ticket
        if not ticket_exists:
            pass
            if not account_data:
                return render_template('CT_Ticket.html', account=[])
            else:
                return render_template('CT_Ticket.html',
                                       account=account_data)
        else:
            return render_template('CT_Ticket.html', account=account_data, existingTicket=ticket_exists)
    else:
        return redirect(url_for('customer_tracking_login'))


### create blank ticket ###
@app.route("/ticket")
def create_ticket():
    if 'username' in session:
        return render_template('CT_Ticket.html',
                               account=[])
    else:
        return redirect(url_for('customer_tracking_login'))


### submit new ticket data into table ###
@app.route("/ticket/submitted", methods=['POST'])
def submit_ticket():
    if 'username' in session:
        data = request.form
        add_ticket_to_db(data, session['username'])
        return render_template('CT_Submitted.html')
    else:
        return redirect(url_for('customer_tracking_login'))
