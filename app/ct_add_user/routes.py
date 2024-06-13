from flask import render_template, request, session, redirect, url_for
from app.ct_add_user.sql import (add_newuser_to_db, update_dept_name_to_id, populate_return_departments, populate_ticket_type, update_ticket_info)
from app import app

### add a new user ###
@app.route("/admin")
def add_new_user():
    if 'username' in session and session['admin'] == 1:
        departments = populate_return_departments()
        currentTicket = populate_ticket_type()

        return render_template('CT_AdminPage.html', deptList=departments, ticketInfo=currentTicket)
    else:
        return redirect(url_for('customer_tracking_login'))


### submit new user to database ###
@app.route("/admin/adduser/submitted", methods=['POST'])
def submit_new_user():
    if 'username' in session and session['admin'] == 1:
        data = request.form
        deptID = update_dept_name_to_id(data['Department'])
        add_newuser_to_db(data, deptID['DeptID'], session['username'])

        return render_template('CT_Submitted.html',
                               newUser=data['UserName'])
    else:
        return redirect(url_for('customer_tracking_login'))


### update ticket type & year in database ###
@app.route("/admin/tickettype/submitted", methods=['POST'])
def update_ticket_type():
    if 'username' in session and session['admin'] == 1:
        data = request.form
        update_ticket_info(data['TicketType'], data['TicketYear'])

        return render_template('CT_Submitted.html',
                               newUser=[])
    else:
        return redirect(url_for('customer_tracking_login'))