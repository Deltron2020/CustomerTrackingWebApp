from DBconnect import coxn
from sqlalchemy import text


### account search for new ticket ###
def load_accounts_from_db(filter_string):
    with coxn.connect() as connection:
        result = connection.execute(
            text(f"SELECT TOP 1000 AccountNumber, PCN, SitusAddress, OwnerName FROM app.CT_Accounts {filter_string} ORDER BY AccountNumber ASC;")
        )
        accounts = []
        for row in result.all():
            accounts.append(dict(row._mapping))
        return accounts


### check to see if ticket for that account already exists ###
def account_ticket_search(account_number):
    with coxn.connect() as connection:
        query = text("SELECT * FROM app.view_CT_Tickets WHERE AccountNumber = :account;")
        result = connection.execute(query, {"account": account_number})

        tickets = []
        for row in result.all():
            tickets.append(dict(row._mapping))
        #print(tickets)
        return tickets


### populate new ticket with account information ###
def populate_ticket_account_data(account_number):
    with coxn.connect() as connection:
        result = connection.execute(
                                    text(f"SELECT AccountNumber, PCN, SitusAddress, OwnerName FROM app.CT_Accounts WHERE AccountNumber = {account_number};")
                                        )
        account = {}
        for row in result.all():
            account.update(dict(row._mapping))
        return account


### insert ticket information into database table ###
def add_ticket_to_db(data, user):
    with coxn.connect() as connection:
        ticketType = connection.execute(text("SELECT TicketType, TicketYear FROM app.CT_TicketType"))
        category = {}
        for value in ticketType.all():
            category.update((dict(value._mapping)))

        query = text(f"INSERT INTO app.CT_Tickets (TicketNumber, AccountNumber, TicketType, TicketYear, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser) VALUES ( NEXT VALUE FOR app.Seq_TicketNumber, {data['Account']}, '{category['TicketType']}', {category['TicketYear']}, '{data['Owner']}', '{data['Address']}', '{data['ContactType']}', '{data['ContactDate']}', '{data['ContactTime']}', '{data['ReturnOperator']}', '{data['CallerVisitor']}', '{data['Telephone']}', '{data['Email']}', '{data['CallReason']}' + ' - {user} - ' + CAST(GETDATE() AS VARCHAR), 'Open', '{user}' );"
                     )
        #print(query)
        connection.execute(query)
        connection.commit()
