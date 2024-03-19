from DBconnect import coxn
from sqlalchemy import text


### account search for new ticket ###
def load_accounts_from_db(filter_string):
    with coxn.connect() as connection:
        result = connection.execute(
            text(f"SELECT TOP 50 AccountNumber, PCN, SitusAddress, OwnerName FROM dbo.accounts {filter_string} ORDER BY AccountNumber ASC;")
        )
        accounts = []
        for row in result.all():
            accounts.append(dict(row._mapping))
        return accounts


### populate new ticket with account information ###
def populate_ticket_account_data(account_number):
    with coxn.connect() as connection:
        result = connection.execute(
                                    text(f"SELECT AccountNumber, PCN, SitusAddress, OwnerName FROM dbo.accounts where AccountNumber = {account_number};")
                                        )
        account = {}
        for row in result.all():
            account.update(dict(row._mapping))
        return account


### insert ticket information into database table ###
def add_ticket_to_db(data, user):
    with coxn.connect() as connection:
        query = text(f"INSERT INTO dbo.CT_Tickets (TicketNumber, AccountNumber, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser) VALUES ((SELECT ID_Value FROM dbo.CT_NextTicketNumber WHERE ID_FieldName = 'TicketNumber'), {data['Account']}, '{data['Owner']}', '{data['Address']}', '{data['ContactType']}', '{data['ContactDate']}', '{data['ContactTime']}', '{data['ReturnOperator']}', '{data['CallerVisitor']}', '{data['Telephone']}', '{data['Email']}', '{data['CallReason']}' + ' - {user} - ' + CAST(GETDATE() AS VARCHAR), 'Open', '{user}');"
                     )
        #print(query)
        connection.execute(query)
        connection.commit()
