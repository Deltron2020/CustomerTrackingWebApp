from flask import Flask, render_template, jsonify, request
from DBinteraction import (load_accounts_from_db, populate_ticket_account_data, add_ticket_to_db,
                           load_tickets_from_db, update_ticket_in_db)

#app = Flask(__name__)


### home ###
@app.route("/")
def customer_tracking():
    return render_template('/app/templates/CT_Home.html',
                           company_name='Property Appraiser')


### ticket search ###
@app.route("/search", methods=['GET'])
def customer_tracking_search():
    data = request.args
    ticket = {}
    for i in data:
        if (len(data[i])) > 0:
            search = {i: data[i]}
            ticket.update(search)
            #print(ticket)
            break

    results = []
    for i in ticket:
        results = load_tickets_from_db(i, ticket[i])

    return render_template('CT_Search.html',
                           ticket_data=results)


### populate existing ticket to be updated ###
@app.route("/search/<ticketNumber>")
def view_searched_ticket(ticketNumber):
    ticket = load_tickets_from_db('TicketNumber', ticketNumber)

    #print(ticket)
    return render_template('CT_UpdateTicket.Html',
                           ticket_data=ticket)


### submit update existing ticket ###
@app.route("/ticket/update_submitted", methods=['POST'])
def update_ticket():
    data = request.form
    update_ticket_in_db(data)
    return render_template('CT_Submitted.html')


### locate account & create ticket ###
@app.route("/create", methods=['GET'])
def customer_tracking_create():
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


### create ticket w account data ###
@app.route("/ticket/<account>")
def create_ticket_for_account(account):
    account_data = populate_ticket_account_data(account)
    if not account_data:
        return render_template('CT_Ticket.html')

    #print(account_data)
    return render_template('CT_Ticket.html',
                           account=account_data)


### create blank ticket ###
@app.route("/ticket")
def create_ticket():
    return render_template('CT_Ticket.html',
                           account=[])


### submit new ticket data into table ###
@app.route("/ticket/submitted", methods=['POST'])
def submit_ticket():
    data = request.form
    add_ticket_to_db(data)
    return render_template('CT_Submitted.html')


print(__name__)
if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)