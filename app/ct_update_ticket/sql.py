from DBconnect import coxn
from sqlalchemy import text


### ticket search ###
def load_tickets_from_db(columns, values):
    with coxn.connect() as connection:
        query = text(f"SELECT TOP 1000 * FROM app.view_CT_Tickets WHERE {columns} ORDER BY TicketNumber ASC;")
        #print(query, values)
        results = connection.execute(query, values)

        tickets = []
        for row in results.all():
            tickets.append(dict(row._mapping))
        #print(tickets)
        return tickets


### insert ticket information into database table (but updating an existing ticket) ###
def update_ticket_in_db(data, user):
    with coxn.connect() as connection:
        checkbox = {}
        # when reading old tickets where the hurricane value is NULL set to 0 on update
        if data['Hurricane'] == 'None':
            checkbox.update({'Hurricane': '0'})
        else:
            checkbox.update({'Hurricane': data['Hurricane']})

        query = text(f"INSERT INTO app.CT_Tickets (TicketNumber, AccountNumber, TicketType, TicketYear, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser, Hurricane) VALUES  (:ticketNumber, :accountNumber, :ticketType, :ticketYear, :ownerName, :situsAddress, :contactType, :contactDate, :contactTime, :returnOperator, :callerVisitor, :phoneNumber, :emailAddress, :reasonForCall, :status, :createUser, :hurricane);"
                     )
        #print(query)
        connection.execute(query, {"ticketNumber": data['TicketNumber'], "accountNumber": data['Account'], "ticketType": data['TicketType'], "ticketYear": data['TicketYear'], "ownerName": data['Owner'], "situsAddress": data['Address'], "contactType": data['ContactType'], "contactDate": data['ContactDate'], "contactTime": data['ContactTime'], "returnOperator": data['ReturnOperator'], "callerVisitor": data['CallerVisitor'], "phoneNumber": data['Telephone'], "emailAddress": data['Email'], "reasonForCall": data['CallReason'], "status": data['Status'], "createUser": user, "hurricane": checkbox['Hurricane']})
        connection.commit()


### check version id before ticket update ###
def version_id_check(data):
    with coxn.connect() as connection:
        query = text(f"SELECT id FROM app.view_CT_Tickets WHERE TicketNumber = :data")
        result = connection.execute(query, {'data': data['TicketNumber']})
        vid = {}
        for row in result.all():
            vid.update(dict(row._mapping))

        return vid


### populate contact types drop down selection ###
def populate_type_of_contact_selection():
    with coxn.connect() as connection:
        query = text("SELECT ContactDescription FROM app.CT_ListContactTypes ORDER BY ContactDescription ASC;")
        result = connection.execute(query)

        types = []
        for data in result.all():
            types.append(data[0])
        return types


### populate return call operator drop down selection ###
def populate_return_call_operator_selection():
    with coxn.connect() as connection:
        query = text("""
            SELECT EmployeeDepartment FROM [app].[view_CT_UserDepts] 
            ORDER BY CASE 
                WHEN EmployeeDepartment = '' THEN 1 
                WHEN EmployeeDepartment = 'All-General' THEN 2
                ELSE 3 END, OrderVal DESC, EmployeeDepartment ASC;
            """)
        results = connection.execute(query)

        operators = []
        for user in results.all():
            operators.append(user[0])
        return operators


### populate got it operator drop down selection ###
def populate_got_it_operator_selection():
    with coxn.connect() as connection:
        query = text("""
        SELECT ed.EmployeeDepartment FROM (

            SELECT EmployeeDepartment, OrderVal FROM [app].[view_CT_UserDepts]
            WHERE EmployeeDepartment NOT LIKE 'test'

			UNION

			SELECT 'None', 0
		) AS ed

            ORDER BY CASE 
                WHEN EmployeeDepartment = '' THEN 1
				WHEN EmployeeDepartment = 'None' THEN 2
                WHEN EmployeeDepartment = 'All-General' THEN 3
                ELSE 4 END, OrderVal DESC, EmployeeDepartment ASC;
            """)
        results = connection.execute(query)

        gotIts = []
        for user in results.all():
            gotIts.append(user[0])
        return gotIts


### populate ticket status drop down selection ###
def populate_ticket_status_selection():
    with coxn.connect() as connection:
        query = text("SELECT StatusDescription FROM app.CT_ListTicketStatus ORDER BY StatusDescription ASC;")
        result = connection.execute(query)

        types = []
        for data in result.all():
            types.append(data[0])
        return types


### check last got it record ###
def check_last_got_it(data):
    with coxn.connect() as connection:
        query = text("SELECT ActionType FROM app.CT_GotItTracking WHERE TicketNumber = :ticketNumber ORDER BY id DESC OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY;")
        result = connection.execute(query, {'ticketNumber': data})

        action = {}
        for row in result.all():
            action.update(dict(row._mapping))

        return action


### insert got it table record ###
def got_it_db_insert(data, action, user, forward):
    if action == 'GOT IT':
        forward = None

    with coxn.connect() as connection:
        query = text("""
                INSERT INTO [app].[CT_GotItTracking]
                   ([TicketNumber]
                   ,[GotItUser]
                   ,[CreateDate]
                   ,[ActionType]
                   ,[ForwardToUser])
             VALUES
                   (:ticketNumber
                   ,:gotItUser
                   ,GETDATE()
                   ,:actionType
                   ,:forwardUser)
                """)

        connection.execute(query, {'ticketNumber': data, 'gotItUser': user, 'actionType': action, 'forwardUser': forward})
        connection.commit()


## got it individual ticket tracking ###
def got_it_ticket_tracking(data):
    with coxn.connect() as connection:
        query = text("SELECT GotItUser, FORMAT(CreateDate,   'MM-dd-yyyy hh:mm:ss tt') AS CreateDate, ActionType, ForwardToUser FROM [app].[CT_GotItTracking] WHERE TicketNumber = :ticketNumber ORDER BY id DESC")
        results = connection.execute(query, {'ticketNumber': data})

        history = []
        for gotit in results.all():
            history.append(dict(gotit._mapping))
        return history


## forward to user ticket tracking ##
def forward_to_options():
    with coxn.connect() as connection:
        query = text("""
            SELECT EmployeeDepartment FROM [app].[view_CT_UserDepts] 
            ORDER BY CASE 
                WHEN EmployeeDepartment = '' THEN 1 
                WHEN EmployeeDepartment = 'All-General' THEN 2
                ELSE 3 END, OrderVal DESC, EmployeeDepartment ASC;
            """)
        results = connection.execute(query)

        forwards = []
        for user in results.all():
            forwards.append(user[0])
        #print(forwards)
        return forwards


## correspondence notes database read ##
def load_correspondence_notes(data):
    with coxn.connect() as connection:
        query = text("SELECT Notes, FORMAT(CreateDate,   'MM-dd-yyyy hh:mm:ss tt') AS CreateDate, CreateUser FROM [app].[CT_CorrespondenceNotes] WHERE TicketNumber = :ticketNumber ORDER BY id DESC")
        results = connection.execute(query, {'ticketNumber': data})

        notes = []
        for note in results.all():
            notes.append(dict(note._mapping))
        return notes


### insert correspondence notes table record ###
def insert_correspondence_notes(data, notes, user):
    with coxn.connect() as connection:
        query = text("""
                INSERT INTO [app].[CT_CorrespondenceNotes]
                   ([TicketNumber]
                   ,[Notes]
                   ,[CreateDate]
                   ,[CreateUser])
             VALUES
                   (:ticketNumber
                   ,:corNotes
                   ,GETDATE()
                   ,:createUser)
                """)

        connection.execute(query, {'ticketNumber': data, 'corNotes': notes, 'createUser': user})
        connection.commit()


def populate_all_ticket_types():
    with coxn.connect() as connection:
        query = text(f"SELECT TicketType FROM app.view_CT_Tickets GROUP BY TicketType ORDER BY CASE WHEN TicketType = (SELECT TicketType FROM app.CT_TicketType) THEN 1 ELSE 2 END;")
        result = connection.execute(query)

        ticketTypes = []
        for data in result.all():
            ticketTypes.append(data[0])

        return ticketTypes


def populate_all_ticket_years():
    with coxn.connect() as connection:
        query = text(f"SELECT TicketYear FROM app.view_CT_Tickets GROUP BY TicketYear ORDER BY CASE WHEN TicketYear = (SELECT TicketYear FROM app.CT_TicketType) THEN 1 ELSE 2 END;")
        result = connection.execute(query)

        ticketYears = []
        for data in result.all():
            ticketYears.append(data[0])

        return ticketYears


def is_personal_property(account):
    with coxn.connect() as connection:
        query = text("""
        IF EXISTS (SELECT IsPersonalProperty FROM app.CT_Accounts WHERE AccountNumber = :accountNumber)
        BEGIN
            SELECT IsPersonalProperty FROM app.CT_Accounts WHERE AccountNumber = :accountNumber;
        END
        ELSE
        BEGIN
            SELECT 0 AS [IsPersonalProperty];
        END
        """)
        result = connection.execute(query, {'accountNumber': account})

        flag = result.all()[0][0]

        return flag


def populate_employee_departments():
    with coxn.connect() as connection:
        query = text("SELECT EmployeeDepartment FROM app.CT_Departments ORDER BY EmployeeDepartment ASC;")
        result = connection.execute(query)

        depts = []
        for data in result.all():
            depts.append(data[0])

        return depts


def populate_created_by():
    with coxn.connect() as connection:
        query = text("""
        SELECT Username FROM app.CT_Users WHERE Username NOT LIKE 'test'
        UNION
        SELECT ''
        ORDER BY Username ASC;
        """)
        result = connection.execute(query)

        users = []
        for data in result.all():
            users.append(data[0])

        return users
