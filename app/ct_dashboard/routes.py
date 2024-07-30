from flask import render_template, request, session, redirect, url_for, jsonify
from app.ct_dashboard.sql import (populate_ticket_type, populate_ticket_year, get_ticket_status_counts, get_contact_type_counts, get_current_type_and_year, get_ticket_created_counts)
from app import app


@app.route("/dashboard")
def populate_dashboard():
    try:
        if 'username' in session and session['admin'] == 1:
            types = populate_ticket_type()
            years = populate_ticket_year()

            current = get_current_type_and_year()
            current[0]['TicketYear'] = str(current[0]['TicketYear'])

            statusTotals = get_ticket_status_counts(current[0]['TicketType'], current[0]['TicketYear'])
            statusLabelsList = list(statusTotals["TicketStatusCounts"].keys())
            statusValuesList = list(statusTotals["TicketStatusCounts"].values())

            contactTypes = get_contact_type_counts(current[0]['TicketType'], current[0]['TicketYear'])
            contactTypeLabelsList = list(contactTypes["ContactTypeCounts"].keys())
            contactTypeValuesList = list(contactTypes["ContactTypeCounts"].values())

            ticketsCreated = get_ticket_created_counts(current[0]['TicketType'], current[0]['TicketYear'])

            return render_template('CT_Dashboard.html', ticketTypes=types, ticketYears=years, statusNames=statusLabelsList, statusNamesValuesList=statusValuesList, contactTypes=contactTypeLabelsList, contactTypeValuesList=contactTypeValuesList,
                                   datesCreated=ticketsCreated['TicketsCreatedCounts']['Dates'], datesCreatedValuesList=ticketsCreated['TicketsCreatedCounts']['Counts'])
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)

@app.route('/dashboard/<ticketYear>/')
@app.route('/dashboard/<ticketYear>/<ticketType>')
def filter_results(ticketType, ticketYear):
    try:
        if 'username' in session:
            print(ticketType, ticketYear)
            statusTotals = get_ticket_status_counts(ticketType, ticketYear)
            contactTotals = get_contact_type_counts(ticketType, ticketYear)
            ticketsCreated = get_ticket_created_counts(ticketType, ticketYear)
            print(ticketsCreated)


            dashboardResults = statusTotals | contactTotals | ticketsCreated

            json = jsonify(dashboardResults).data

            return json

        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)
