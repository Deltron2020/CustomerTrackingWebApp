from DBconnect import coxn
from sqlalchemy import text


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