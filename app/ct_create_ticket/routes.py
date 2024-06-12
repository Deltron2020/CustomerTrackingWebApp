from flask import render_template, request, session, redirect, url_for
from app.ct_create_ticket.sql import (load_accounts_from_db, populate_ticket_account_data, add_ticket_to_db, account_ticket_search, populate_type_of_contact_selection, populate_return_call_operator_selection, populate_ticket_status_selection)
from app import app


### locate account (account search) ###
@app.route("/create", methods=['GET'])
def customer_tracking_create():
    if 'username' in session:
        account = {}
        for i in request.args:         # data returned from inputs (4 possible fields)
            if request.args.get('AccountNumber') != '':
                account.update({'AccountNumber': request.args.get('AccountNumber')})
                break
            if request.args.get('PCN') != '':
                account.update({'PCN': request.args.get('PCN')})
                break
            if request.args.get('SitusAddress') != '':
                account.update({'SitusAddress': request.args.get('SitusAddress')})
                break
            if request.args.get('OwnerName') != '':
                account.update({'OwnerName': request.args.get('OwnerName')})
                break

        if not account:
            results = []
            return render_template('CT_Create.html',
                               account_data=results)
        else:
            field = [key for key in account.keys()][0]
            value = [val for val in account.values()][0]
            results = load_accounts_from_db(field, value)
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
        contact_types = populate_type_of_contact_selection()
        return_operators = populate_return_call_operator_selection()
        status_options = populate_ticket_status_selection()
        if not ticket_exists:
            pass
            if not account_data:
                return render_template('CT_Ticket.html', account=[], contact_types=contact_types, return_operators=return_operators, status_options=status_options)
            else:
                return render_template('CT_Ticket.html',
                                       account=account_data, contact_types=contact_types, return_operators=return_operators, status_options=status_options)
        else:
            return render_template('CT_Ticket.html', account=account_data, existingTicket=ticket_exists, contact_types=contact_types, return_operators=return_operators, status_options=status_options)
    else:
        return redirect(url_for('customer_tracking_login'))


### create blank ticket ###
@app.route("/ticket")
def create_ticket():
    if 'username' in session:
        contact_types = populate_type_of_contact_selection()
        return_operators = populate_return_call_operator_selection()
        status_options = populate_ticket_status_selection()
        return render_template('CT_Ticket.html',
                               account=[],
                               contact_types=contact_types,
                               return_operators=return_operators,
                               status_options=status_options)
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
