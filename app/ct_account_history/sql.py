from DBconnect import coxn
from sqlalchemy import text


### ticket history for account query ###
def load_account_ticket_history_from_db(account):
    with coxn.connect() as connection:
        query = text("""
        SELECT
            t.TicketNumber,
            t.TicketType,
            t.TicketYear,
            t.ContactDate,
            t.ContactType,
            t.Status,
            t.CreateDateTime
        FROM 
            app.view_CT_Tickets t
        JOIN 
            app.CT_Accounts a ON a.AccountNumber = t.AccountNumber
        WHERE 
            t.AccountNumber = :accountNumber
        AND
            t.TicketType <> 'Testing'
        ORDER BY
            t.TicketNumber ASC;
        """)

        result = connection.execute(query, {"accountNumber": account})
        ticketHistory = []

        for row in result.all():
            ticketHistory.append(dict(row._mapping))

        return ticketHistory


### account search query ###
def load_account_from_db(account):
    with coxn.connect() as connection:
        query = text(f"SELECT AccountNumber, PCN, SitusAddress, OwnerName FROM app.CT_Accounts WHERE AccountNumber = :accountNumber;")
        result = connection.execute(query, {"accountNumber": account})
        accountData = []

        for row in result.all():
            accountData.append(dict(row._mapping))

        return accountData
