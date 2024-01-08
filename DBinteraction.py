# DBinteraction.py
from DBconnect import coxn
from sqlalchemy import Table, Column, Integer, String, MetaData, text

### This script contains all of the sql queries - reading and writing data ###


### populate new ticket with account information ###
def populate_ticket_account_data(account_number):
    with coxn.connect() as connection:
        result = connection.execute(
                                    text("select AccountNumber, PCN, SitusAddress, OwnerName from dbo.accounts where AccountNumber = %s;"
                                        % account_number)
                                        )
        account = {}
        for row in result.all():
            account.update(dict(row._mapping))
        return account


### account search for new ticket ###
def load_accounts_from_db(field, value):
    with coxn.connect() as connection:
        result = connection.execute(
            text("select TOP 25 AccountNumber, PCN, SitusAddress, OwnerName from dbo.accounts where %s LIKE %s ORDER BY AccountNumber;"
                % (field, "'%" + str(value) + "%'"))
        )
        accounts = []
        for row in result.all():
            accounts.append(dict(row._mapping))
        #print(accounts)
        return accounts


### ticket search ###
def load_tickets_from_db(field, value):
    with coxn.connect() as connection:
        result = connection.execute(
            text(
                "SELECT TOP 25 t.TicketNumber, AccountNumber, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CONVERT(NVARCHAR, CreateDateTime, 0) AS CreateDateTime FROM dbo.CT_Tickets t JOIN (SELECT TicketNumber, MAX(id) AS VersionID FROM CT_Tickets GROUP BY TicketNumber) tm ON tm.VersionID = t.id AND tm.TicketNumber = t.TicketNumber WHERE t.%s LIKE %s ORDER BY t.TicketNumber ASC, t.ContactDate ASC, t.AccountNumber ASC;"
                % (field, "'%" + str(value) + "%'"))
        )
        tickets = []
        for row in result.all():
            tickets.append(dict(row._mapping))
        #print(tickets)
        return tickets


### insert ticket information into database table ###
def add_ticket_to_db(data):
    with coxn.connect() as connection:
        query = text("INSERT INTO dbo.CT_Tickets (TicketNumber, AccountNumber, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status) VALUES ((SELECT ID_Value FROM dbo.CT_NextTicketNumber WHERE ID_FieldName = 'TicketNumber'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                     % ( data['Account'], "'" + str(data['Owner']) + "'", "'" + str(data['Address']) + "'", "'" + str(data['ContactType']) + "'", "'" + str(data['ContactDate']) + "'", "'" + str(data['ContactTime']) + "'", "'" + str(data['ReturnOperator']) + "'", "'" + str(data['CallerVisitor']) + "'",
                         "'" + str(data['Telephone']) + "'", "'" + str(data['Email']) + "'", "'" + str(data['CallReason']) + "'", "'" + str('Open') + "'")
                     )
        #print(query)
        connection.execute(query)
        connection.commit()


### insert ticket information into database table (but updating an existing ticket) ###
def update_ticket_in_db(data):
    with coxn.connect() as connection:
        query = text("INSERT INTO dbo.CT_Tickets (TicketNumber, AccountNumber, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, LTRIM(%s), %s);"
                     % ( data['TicketNumber'], data['Account'], "'" + str(data['Owner']) + "'", "'" + str(data['Address']) + "'", "'" + str(data['ContactType']) + "'", "'" + str(data['ContactDate']) + "'", "'" + str(data['ContactTime']) + "'", "'" + str(data['ReturnOperator']) + "'", "'" + str(data['CallerVisitor']) + "'",
                         "'" + str(data['Telephone']) + "'", "'" + str(data['Email']) + "'", "'" + str(data['CallReason']) + "'", "'" + str(data['Status']) + "'")
                     )
        #print(query)
        connection.execute(query)
        connection.commit()