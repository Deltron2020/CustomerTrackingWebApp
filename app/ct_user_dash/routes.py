from flask import render_template, request, session, redirect, url_for
from app.ct_user_dash.sql import (populate_user_dash_info, populate_ticket_year_and_type_info, populate_tickets_created_count, populate_tickets_worked_count, load_user_dash_ticket_history_from_db, load_dept_dash_ticket_history_from_db, populate_user_dash_chart)
from app import app


### locate account (account search) ###
@app.route("/userDash")
def user_ticket_dashboard():
    try:
        if 'username' in session:

            user_info = populate_user_dash_info(session['username'])
            ticket_info = populate_ticket_year_and_type_info()
            created_count = populate_tickets_created_count(session['username'])
            worked_count = populate_tickets_worked_count(session['username'])
            user_tickets = load_user_dash_ticket_history_from_db(session['username'])
            dept_tickets = load_dept_dash_ticket_history_from_db(user_info['EmployeeDepartment'])
            user_data = populate_user_dash_chart(session['username'])
            categories = []
            created_counts = []
            worked_counts = []
            for i in user_data:
                categories.append([i['TicketType'], i['TicketYear']])
                created_counts.append(i['TicketsCreatedCount'])
                worked_counts.append(i['TicketsWorkedCount'])

            return render_template('CT_UserDash.html', user_info=user_info, ticket_info=ticket_info, created_count=created_count, worked_count=worked_count, user_tickets=user_tickets, dept_tickets=dept_tickets, categories=categories, created_counts=created_counts, worked_counts=worked_counts)
        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)