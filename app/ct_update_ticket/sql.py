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
            query = text(f"INSERT INTO app.CT_Tickets (TicketNumber, AccountNumber, TicketType, TicketYear, OwnerName, SitusAddress, ContactType, ContactDate, ContactTime, ReturnOperator, CallerOrVisitor, PhoneNumber, EmailAddress, ReasonForCall, Status, CreateUser) VALUES ({data['TicketNumber']}, {data['Account']}, '{data['TicketType']}', {data['TicketYear']}, '{data['Owner']}', '{data['Address']}', '{data['ContactType']}', '{data['ContactDate']}', '{data['ContactTime']}', '{data['ReturnOperator']}', '{data['CallerVisitor']}', '{data['Telephone']}', '{data['Email']}', RTRIM(LTRIM('{data['CallReason']}')) + ' - {user} - ' + CAST(GETDATE() AS VARCHAR), '{data['Status']}', '{data['CreateUser']}');"
                         )
            #print(query)
            connection.execute(query)
            connection.commit()


### check version id before ticket update ###
def version_id_check(data):
    with coxn.connect() as connection:
        query = text(f"SELECT id FROM app.view_CT_Tickets WHERE TicketNumber = {data['TicketNumber']}")
        result = connection.execute(query)

        vid = {}
        for row in result.all():
            vid.update(dict(row._mapping))

        return vid


### insert got it table record ###
def got_it_db_insert(data, user):
    with coxn.connect() as connection:
        query = text("""
                INSERT INTO [app].[CT_GotItTracking]
                   ([TicketNumber]
                   ,[GotItUser]
                   ,[CreateDate])
             VALUES
                   (:ticketNumber
                   ,:gotItUser
                   ,GETDATE())
                """)

        connection.execute(query, {'ticketNumber': data, 'gotItUser': user})
        connection.commit()


## got it individual ticket tracking ###
def got_it_ticket_tracking(data):
    with coxn.connect() as connection:
        query = text("SELECT GotItUser, CreateDate FROM [app].[CT_GotItTracking] WHERE TicketNumber = :ticketNumber ORDER BY id DESC")
        results = connection.execute(query, {'ticketNumber': data})

        history = []
        for gotit in results.all():
            history.append(dict(gotit._mapping))
        return history
