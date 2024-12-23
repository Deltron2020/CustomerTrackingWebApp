from flask import render_template, request, session, redirect, url_for, jsonify, flash
import json
from app.ct_update_ticket.sql import (load_tickets_from_db, update_ticket_in_db, version_id_check, got_it_db_insert, got_it_ticket_tracking, forward_to_options, insert_correspondence_notes, load_correspondence_notes, populate_type_of_contact_selection, populate_return_call_operator_selection, populate_ticket_status_selection, populate_all_ticket_types, populate_got_it_operator_selection, check_last_got_it, populate_all_ticket_years, is_personal_property, populate_employee_departments, populate_created_by)
from app import app


### ticket search ###
@app.route("/search", methods=['GET'])
def customer_tracking_search():
    try:
        if 'username' in session:
            contact_types = populate_type_of_contact_selection()
            #return_operators = populate_return_call_operator_selection()
            create_users = populate_created_by()
            employee_depts = populate_employee_departments()
            gotit_operators = populate_got_it_operator_selection()
            status_options = populate_ticket_status_selection()
            ticketTypes = populate_all_ticket_types()
            ticketYears = populate_all_ticket_years()

            return render_template('CT_Search.html',
                                   current_user=session['username'],
                                   contact_types=contact_types,
                                   #return_operators=return_operators,
                                   gotit_operators=gotit_operators,
                                   status_options=status_options,
                                   ticketTypes=ticketTypes,
                                   ticketYears=ticketYears,
                                   create_users=create_users,
                                   employee_depts=employee_depts)

        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)


### populate existing ticket to be updated ###
@app.route("/search/<ticketNumber>")
def view_searched_ticket(ticketNumber):
    try:
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
            personal_property_flag = is_personal_property(ticket[0]['AccountNumber'])

            return render_template('CT_UpdateTicket.Html',
                                   ticket_data=ticket,
                                   tracking_data=tracking,
                                   forward_users=forwards,
                                   correspondence_notes=notes,
                                   contact_types=contact_types,
                                   return_operators=return_operators,
                                   status_options=status_options,
                                   personal_property=personal_property_flag)
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)


### submit update existing ticket ###
@app.route("/ticket/update_submitted", methods=['POST'])
def update_ticket():
    try:
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
    except Exception as e:
        return render_template('CT_Error.html', error=e)


## background process happening without any refreshing for got it/forward tracking ##
@app.route('/got_it_update/<ticketNumber>/<action>/<forward>')
def got_it_update(ticketNumber, action, forward):
    try:
        if 'username' in session:
            # if Got IT action > if prev record was a GOT IT > notify user and do not insert new GOT IT record
            prevAction = check_last_got_it(ticketNumber)
            if len(prevAction) == 0:
                prevAction = {'ActionType': ''}

            if prevAction['ActionType'] == 'GOT IT' and action == 'GOT IT':
                tracking = got_it_ticket_tracking(ticketNumber)
            else:
                got_it_db_insert(ticketNumber, action, session['username'], forward)
                tracking = got_it_ticket_tracking(ticketNumber)

            json = jsonify(tracking).data
            #print(json)

            return json
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)


## background process happening without any refreshing for correspondence notes ##
@app.route('/got_it_update/notes_submitted/<ticketNumber>', methods=['POST'])
def correspondence_notes_update(ticketNumber):
    try:
        if 'username' in session:
            data = request.form
            #print(data['CorrespondenceNotes'])
            insert_correspondence_notes(ticketNumber, data['CorrespondenceNotes'], session['username'])
            return (
                redirect(url_for('view_searched_ticket', ticketNumber=ticketNumber)))

        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)


# json search functionality
@app.route("/searchjson", methods=['GET'])
def customer_tracking_search_test_json():
    try:
        if 'username' in session:
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

            if 'PhoneNumber' in columns:
                columns = columns.replace('PhoneNumber', r"TRIM(REPLACE(REPLACE(REPLACE(REPLACE(PhoneNumber,' ',''),')',''),'(',''),'-',''))")

            results = load_tickets_from_db(columns, parameters)

            json_data = json.dumps(results, indent=4, sort_keys=True, default=str)

            return json_data

        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)