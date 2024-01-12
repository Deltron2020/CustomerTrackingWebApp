from flask import render_template, request
from app.ct_update_ticket.sql import (load_tickets_from_db, update_ticket_in_db)
from app import app


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