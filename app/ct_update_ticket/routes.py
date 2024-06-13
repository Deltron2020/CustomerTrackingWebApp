from flask import render_template, request, session, redirect, url_for, jsonify, flash
from app.ct_update_ticket.sql import (load_tickets_from_db, update_ticket_in_db, version_id_check, got_it_db_insert, got_it_ticket_tracking, forward_to_options, insert_correspondence_notes, load_correspondence_notes, populate_type_of_contact_selection, populate_return_call_operator_selection, populate_ticket_status_selection, populate_all_ticket_types)
from app import app
from datetime import date, timedelta


### ticket search ###
@app.route("/search", methods=['GET'])
def customer_tracking_search():
    if 'username' in session:
        contact_types = populate_type_of_contact_selection()
        return_operators = populate_return_call_operator_selection()
        status_options = populate_ticket_status_selection()
        ticketTypes = populate_all_ticket_types()
        data = request.args
        ticket = {}
        for i in data:
            if (len(data[i])) > 0:
                search = {i: data[i]}
                ticket.update(search)

        columns = ' AND '.join(f"{column} LIKE :?" for column in ticket.keys())
        for i in ticket:
            columns = columns.replace('?', str(ticket[i]).replace('-','').replace(' ',''), 1)

        parameters = {}
        for val in ticket.values():
            parameters.update({val.replace('-','').replace(' ',''): '%'+val+'%'})

        if not ticket:
            results = []
            return render_template('CT_Search.html',
                                   ticket_data=results,
                                   current_user=session['username'],
                                   contact_types=contact_types,
                                   return_operators=return_operators,
                                   status_options=status_options,
                                   ticketTypes=ticketTypes)
        else:
            results = load_tickets_from_db(columns, parameters)
            return render_template('CT_Search.html',
                                   ticket_data=results,
                                   current_user=session['username'],
                                   current_date=date.today() - timedelta(days=3),
                                   contact_types=contact_types,
                                   return_operators=return_operators,
                                   status_options=status_options,
                                   ticketTypes=ticketTypes)

    else:
        return redirect(url_for('customer_tracking_login'))


### populate existing ticket to be updated ###
@app.route("/search/<ticketNumber>")
def view_searched_ticket(ticketNumber):
    if 'username' in session:
        ticket_filter = "TicketNumber = :value"
        ticket_dict = {'value': ticketNumber}

        ticket = load_tickets_from_db(ticket_filter,ticket_dict)
        tracking = got_it_ticket_tracking(ticketNumber)
        contact_types = populate_type_of_contact_selection()
        return_operators = populate_return_call_operator_selection()
        status_options = populate_ticket_status_selection()
        forwards = forward_to_options()
        notes = load_correspondence_notes(ticketNumber)

        return render_template('CT_UpdateTicket.Html',
                               ticket_data=ticket,
                               tracking_data=tracking,
                               forward_users=forwards,
                               correspondence_notes=notes,
                               contact_types=contact_types,
                               return_operators=return_operators,
                               status_options=status_options)
    else:
        return redirect(url_for('customer_tracking_login'))


### submit update existing ticket ###
@app.route("/ticket/update_submitted", methods=['POST'])
def update_ticket():
    if 'username' in session:
        data = request.form
        version = version_id_check(data)

        if int(version['id']) != int(data['id']):
            flash('This ticket has been updated since you originally viewed it, please review the changes and try again.', category='error')
            return (
                redirect(url_for('view_searched_ticket', ticketNumber=data['TicketNumber'])))

        else:
            update_ticket_in_db(data, session['username'])
            return render_template('CT_Submitted.html')

    else:
        return redirect(url_for('customer_tracking_login'))


## background process happening without any refreshing for got it/forward tracking ##
@app.route('/got_it_update/<ticketNumber>/<action>/<forward>')
def got_it_update(ticketNumber, action, forward):
    if 'username' in session:
        got_it_db_insert(ticketNumber, action, session['username'], forward)
        tracking = got_it_ticket_tracking(ticketNumber)
        json = jsonify(tracking).data

        return json
    else:
        return redirect(url_for('customer_tracking_login'))


## background process happening without any refreshing for correspondence notes ##
@app.route('/got_it_update/notes_submitted/<ticketNumber>', methods=['POST'])
def correspondence_notes_update(ticketNumber):
    if 'username' in session:
        data = request.form
        #print(data['CorrespondenceNotes'])
        insert_correspondence_notes(ticketNumber, data['CorrespondenceNotes'], session['username'])
        return (
            redirect(url_for('view_searched_ticket', ticketNumber=ticketNumber)))

    else:
        return redirect(url_for('customer_tracking_login'))
