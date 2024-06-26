from DBconnect import coxn
from sqlalchemy import text


### account search for new ticket ###
def load_accounts_from_db(field, value):
    with coxn.connect() as connection:
        query = text(f"SELECT TOP 1000 AccountNumber, PCN, SitusAddress, OwnerName FROM app.CT_Accounts WHERE {field} LIKE '%' + :dataValue + '%' ORDER BY AccountNumber ASC;")
        result = connection.execute(query, {"dataValue": value})
        accounts = []
        for row in result.all():
            accounts.append(dict(row._mapping))
        return accounts


### check to see if ticket for that account already exists ###
def account_ticket_search(account_number):
    with coxn.connect() as connection:
        query = text("SELECT TicketNumber FROM app.view_CT_Tickets vt JOIN app.CT_TicketType tt ON tt.TicketType = vt.TicketType AND tt.TicketYear = vt.TicketYear WHERE AccountNumber = :account AND Status IN ('Open', 'Pending') ORDER BY vt.id DESC;")
        result = connection.execute(query, {"account": account_number})

        tickets = []
        for row in result.all():
            tickets.append(dict(row._mapping))
        #print(tickets)
        return tickets


### populate new ticket with account information ###
def populate_ticket_account_data(account_number):
    with coxn.connect() as connection:
        query = text(f"SELECT AccountNumber, PCN, SitusAddress, OwnerName FROM app.CT_Accounts WHERE AccountNumber = :account;")
        result = connection.execute(query, {"account": account_number})
        account = {}
        for row in result.all():
            account.update(dict(row._mapping))
        return account


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
                WHEN EmployeeDepartment = 'All/General' THEN 2
                ELSE 3 END, OrderVal DESC, EmployeeDepartment ASC;
            """)
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


### insert ticket information into database table ###
def add_ticket_to_db(data, user):
    with coxn.connect() as connection:
        ticketType = connection.execute(text("SELECT TicketType, TicketYear FROM app.CT_TicketType"))
        category = {}
        for value in ticketType.all():
            category.update((dict(value._mapping)))

        query = text(f"INSERT INTO app.CT_Tickets (TicketNumber, AccountNumber, TicketType, TicketYear, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser) VALUES ( NEXT VALUE FOR app.Seq_TicketNumber, :account, :ticketType, :ticketYear, :owner, :address, :contactType, :contactDate, :contactTime, :returnOperator, :callerVisitor, :telephone, :email, :reasonForCall, :status, :createUser );"
                     )
        #print(query)
        connection.execute(query, {"account": data['Account'], "ticketType": category['TicketType'], "ticketYear": category['TicketYear'], "owner": data['Owner'], "address": data['Address'], "contactType": data['ContactType'], "contactDate": data['ContactDate'], "contactTime": data['ContactTime'], "returnOperator": data['ReturnOperator'], "callerVisitor": data['CallerVisitor'], "telephone": data['Telephone'], "email": data['Email'], "reasonForCall": data['CallReason'], "status": data['Status'], "createUser": user})
        connection.commit()
