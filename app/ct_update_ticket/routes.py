from flask import render_template, request, session, redirect, url_for, jsonify
from app.ct_update_ticket.sql import (load_tickets_from_db, update_ticket_in_db, version_id_check, got_it_db_insert, got_it_ticket_tracking, forward_to_options)
from app import app


### ticket search ###
@app.route("/search", methods=['GET'])
def customer_tracking_search():
    if 'username' in session:
        data = request.args
        ticket = {}
        for i in data:
            if (len(data[i])) > 0:
                search = {i: data[i]}
                ticket.update(search)

        query_filter = ''
        for e, field in enumerate(ticket):
            if e == 0:
                query_filter += (f"WHERE {field} LIKE '%{ticket[field]}%'")
            elif e >= 1:
                query_filter += (f" AND {field} LIKE '%{ticket[field]}%'")

        if not query_filter:
            results = []
            return render_template('CT_Search.html',
                                   ticket_data=results,
                                   current_user=session['username'])
        else:
            results = load_tickets_from_db(query_filter)
            return render_template('CT_Search.html',
                                   ticket_data=results,
                                   current_user=session['username'])

    else:
        return redirect(url_for('customer_tracking_login'))


### populate existing ticket to be updated ###
@app.route("/search/<ticketNumber>")
def view_searched_ticket(ticketNumber):
    if 'username' in session:
        ticket_filter = f"WHERE TicketNumber = {ticketNumber}"
        ticket = load_tickets_from_db(ticket_filter)
        tracking = got_it_ticket_tracking(ticketNumber)
        forwards = forward_to_options()

        return render_template('CT_UpdateTicket.Html',
                               ticket_data=ticket,
                               tracking_data=tracking,
                               forward_users=forwards)
    else:
        return redirect(url_for('customer_tracking_login'))


### submit update existing ticket ###
@app.route("/ticket/update_submitted", methods=['POST'])
def update_ticket():
    if 'username' in session:
        data = request.form

        version = version_id_check(data)

        if int(version['id']) != int(data['id']):
            ticket_filter = f"WHERE TicketNumber = {data['TicketNumber']}"
            ticket = load_tickets_from_db(ticket_filter)
            return render_template('CT_UpdateTicket.Html', ticket_data=ticket, reloaded_ticket=1)

        else:
            update_ticket_in_db(data, session['username'])
            return render_template('CT_Submitted.html')

    else:
        return redirect(url_for('customer_tracking_login'))


#background process happening without any refreshing
@app.route('/got_it_update/<ticketNumber>/<action>/<forward>')
def got_it_update(ticketNumber, action, forward):
    if 'username' in session:
        got_it_db_insert(ticketNumber, action, session['username'], forward)
        tracking = got_it_ticket_tracking(ticketNumber)
        json = jsonify(tracking).data

        return json
    else:
        return redirect(url_for('customer_tracking_login'))