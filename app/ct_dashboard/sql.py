from DBconnect import coxn
from sqlalchemy import text

def populate_ticket_type():
    with coxn.connect() as connection:
        query = text("SELECT TicketType FROM app.CT_ListTicketTypes ORDER BY TicketType ASC;")
        results = connection.execute(query)

        ticketType = []
        for row in results.all():
            ticketType.append(row[0])

        return ticketType


def populate_ticket_year():
    with coxn.connect() as connection:
        query = text("SELECT TicketYear FROM app.CT_ListTicketYears ORDER BY TicketYear DESC;")
        results = connection.execute(query)

        ticketYear = []
        for row in results.all():
            ticketYear.append(row[0])

        return ticketYear


def get_current_type_and_year():
    with coxn.connect() as connection:
        query = text("SELECT TicketType, TicketYear FROM app.CT_TicketType;")
        results = connection.execute(query)

        currentInfo = []
        for info in results.all():
            currentInfo.append(dict(info._mapping))

        return currentInfo


### query for ticket status chart ###
def get_ticket_status_counts(type, year):
    with coxn.connect() as connection:
        query = text("""
            SELECT
                [Status],
				COUNT(Status) AS [TicketStatusCounts]
            FROM
                app.view_CT_Tickets
			WHERE
				TicketType LIKE '%' + :ticketType + '%'
			AND
				TicketYear LIKE '%' + :ticketYear + '%'
            GROUP BY
                [Status];
        """)
        results = connection.execute(query, {'ticketType': type, 'ticketYear': year})

        dict = {}
        for row in results.all():
            count = {row[0]: row[1]}
            dict.update(count)

        dict = {'TicketStatusCounts': dict}

        return dict


### query for contact type chart ###
def get_contact_type_counts(type, year):
    with coxn.connect() as connection:
        query = text("""
            SELECT
                [ContactType],
				COUNT(ContactType) AS [ContactTypeStatusCounts]
            FROM
                app.view_CT_Tickets
			WHERE
				TicketType LIKE '%' + :ticketType + '%'
			AND
				TicketYear LIKE '%' + :ticketYear + '%'
            GROUP BY
                [ContactType];
        """)
        results = connection.execute(query, {'ticketType': type, 'ticketYear': year})

        dict = {}
        for row in results.all():
            count = {row[0]: row[1]}
            dict.update(count)

        dict = {'ContactTypeCounts': dict}

        return dict


### query for timeline of tickets created chart ###
def get_ticket_created_counts(type, year):
    with coxn.connect() as connection:
        query = text("""
            SELECT
                FORMAT(CAST(CreateDateTime AS DATE), 'MM-dd') AS CreateDate, 
                COUNT(TicketNumber) AS [TicketCount]
            FROM 
                app.CT_Tickets
            WHERE
				TicketType LIKE '%' + :ticketType + '%'
			AND
				TicketYear LIKE '%' + :ticketYear + '%'
            GROUP BY
                CAST(CreateDateTime AS DATE)
            ORDER BY 
                CAST(CreateDateTime AS DATE) ASC;
        """)
        results = connection.execute(query, {'ticketType': type, 'ticketYear': year})

        datesList = []
        countsList = []
        for row in results.all():
            datesList.append(row[0])
            countsList.append(row[1])

        dict = {'TicketsCreatedCounts': {'Dates': datesList, 'Counts': countsList}}

        return dict
