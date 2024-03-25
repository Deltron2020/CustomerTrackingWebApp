from DBconnect import coxn
from sqlalchemy import text


### ticket search ###
def load_tickets_from_db(filter_string):
    with coxn.connect() as connection:
        result = connection.execute(
            text(
                f"SELECT TOP 50 * FROM app.view_CT_Tickets {filter_string} ORDER BY TicketNumber ASC;")
        )
        tickets = []
        for row in result.all():
            tickets.append(dict(row._mapping))
        #print(tickets)
        return tickets


### insert ticket information into database table (but updating an existing ticket) ###
def update_ticket_in_db(data, user):
    with coxn.connect() as connection:
        query = text(f"INSERT INTO app.CT_Tickets (TicketNumber, AccountNumber, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser) VALUES ({data['TicketNumber']}, {data['Account']}, '{data['Owner']}', '{data['Address']}', '{data['ContactType']}', '{data['ContactDate']}', '{data['ContactTime']}', '{data['ReturnOperator']}', '{data['CallerVisitor']}', '{data['Telephone']}', '{data['Email']}', RTRIM(LTRIM('{data['CallReason']}')) + ' - {user} - ' + CAST(GETDATE() AS VARCHAR), '{data['Status']}', '{data['CreateUser']}');"
                     )
        #print(query)
        connection.execute(query)
        connection.commit()
