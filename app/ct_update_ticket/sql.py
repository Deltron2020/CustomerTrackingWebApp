from DBconnect import coxn
from sqlalchemy import text


### ticket search ###
def load_tickets_from_db(columns, values):
    with coxn.connect() as connection:
        query = text(f"SELECT TOP 50 * FROM app.view_CT_Tickets WHERE {columns} ORDER BY TicketNumber ASC;")
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
            query = text(f"INSERT INTO app.CT_Tickets (TicketNumber, AccountNumber, TicketType, TicketYear, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser) VALUES  (:ticketNumber, :accountNumber, :ticketType, :ticketYear, :ownerName, :situsAddress, :contactType, :contactDate, :contactTime, :returnOperator, :callerVisitor, :phoneNumber, :emailAddress, :reasonForCall, :status, :createUser);"
                         )
            #print(query)
            connection.execute(query, {"ticketNumber": data['TicketNumber'], "accountNumber": data['Account'], "ticketType": data['TicketType'], "ticketYear": data['TicketYear'], "ownerName": data['Owner'], "situsAddress": data['Address'], "contactType": data['ContactType'], "contactDate": data['ContactDate'], "contactTime": data['ContactTime'], "returnOperator": data['ReturnOperator'], "callerVisitor": data['CallerVisitor'], "phoneNumber": data['Telephone'], "emailAddress": data['Email'], "reasonForCall": data['CallReason'], "status": data['Status'], "createUser": user})

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
        query = text("SELECT EmployeeDepartment FROM [app].[view_CT_UserDepts] ORDER BY EmployeeDepartment ASC;")
        results = connection.execute(query)

        operators = []
        for user in results.all():
            operators.append(user[0])
        return operators


### populate ticket status drop down selection ###
def populate_ticket_status_selection():
    with coxn.connect() as connection:
        query = text("SELECT StatusDescription FROM app.CT_ListTicketStatus ORDER BY StatusDescription ASC;")
        result = connection.execute(query)

        types = []
        for data in result.all():
            types.append(data[0])
        return types


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
        query = text("SELECT EmployeeDepartment FROM [app].[view_CT_UserDepts] ORDER BY EmployeeDepartment ASC;")
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
        query = text(f"SELECT DISTINCT TicketType, TicketYear FROM app.view_CT_Tickets;")
        result = connection.execute(query)

        ticketTypes = []
        for data in result.all():
            ticketTypes.append(data)

        return ticketTypes
