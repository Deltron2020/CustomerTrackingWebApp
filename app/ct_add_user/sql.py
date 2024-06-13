from DBconnect import coxn
from sqlalchemy import text

def add_newuser_to_db(data, deptID, user):
    with coxn.connect() as connection:
        query = text(f"INSERT INTO app.CT_Users ( Username, Password, Email, DeptID, CreateUser) VALUES (:userName, :password, :emailAddress, :department, :createUser);"
                     )

        connection.execute(query, {"userName": data['UserName'], "password": data['Password'], "emailAddress": data['Email'], "department": deptID, "createUser": user})
        connection.commit()


def update_dept_name_to_id(name):
    with coxn.connect() as connection:
        query = text("SELECT DeptID FROM app.CT_Departments WHERE EmployeeDepartment = :employeeDepartment;")
        result = connection.execute(query, {"employeeDepartment": name})

        deptName = {}
        for row in result.all():
            deptName.update(dict(row._mapping))
        print(deptName)
        return deptName


def populate_return_departments():
    with coxn.connect() as connection:
        query = text("SELECT EmployeeDepartment FROM [app].[CT_Departments] ORDER BY EmployeeDepartment ASC;")
        results = connection.execute(query)

        operators = []
        for user in results.all():
            operators.append(user[0])

        return operators


def populate_ticket_type():
    with coxn.connect() as connection:
        query = text("SELECT TicketType, TicketYear FROM app.CT_TicketType;")
        results = connection.execute(query)

        ticket = {}
        for row in results.all():
            ticket.update(dict(row._mapping))\

        print(ticket)
        return ticket


def update_ticket_info(tickettype, ticketyear):
    with coxn.connect() as connection:
        query = text("""
            UPDATE app.CT_TicketType
            SET TicketType = :ticketType,
                TicketYear = :ticketYear;
                """)
        connection.execute(query, {"ticketType": tickettype, "ticketYear": ticketyear})
        connection.commit()
