from DBconnect import coxn
from sqlalchemy import text

def populate_ticket_type():
    with coxn.connect() as connection:
        query = text("SELECT TicketType FROM app.CT_ListTicketTypes ORDER BY CASE WHEN TicketType = (SELECT TicketType FROM app.CT_TicketType) THEN 1 ELSE 2 END;")
        results = connection.execute(query)

        ticketType = []
        for row in results.all():
            ticketType.append(row[0])

        return ticketType


def populate_ticket_year():
    with coxn.connect() as connection:
        query = text("SELECT TicketYear FROM app.CT_ListTicketYears ORDER BY CASE WHEN TicketYear = (SELECT TicketYear FROM app.CT_TicketType) THEN 1 ELSE 2 END;")
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
                s.StatusDescription,
                COUNT(t.TicketNumber) AS [TicketStatusCounts]
            FROM
                app.CT_ListTicketStatus s
            LEFT JOIN
                (SELECT ticketNumber, Status 
                FROM app.view_CT_Tickets 
                WHERE
                TicketType LIKE '%' + :ticketType + '%'
                AND
                TicketYear LIKE '%' + :ticketYear + '%') t ON t.Status = s.StatusDescription
            WHERE
                s.StatusDescription <> ''
            GROUP BY
                s.StatusDescription;
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
                c.ContactDescription,
                COUNT(t.TicketNumber) AS [TicketStatusCounts]
            FROM
                app.CT_ListContactTypes c
            LEFT JOIN
                (SELECT ticketNumber, ContactType 
                FROM app.view_CT_Tickets 
                WHERE
                TicketType LIKE '%' + :ticketType + '%'
                AND
                TicketYear LIKE '%' + :ticketYear + '%') t ON t.ContactType = c.ContactDescription
            WHERE
                c.ContactDescription <> ''
            GROUP BY
                c.ContactDescription;
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
            ;WITH min_id_cte AS
            (
                SELECT
                    TicketNumber,
                    MIN(id) AS [mID]
                FROM
                    app.CT_Tickets
                WHERE
				    TicketType LIKE '%' + :ticketType + '%'
			    AND
				    TicketYear LIKE '%' + :ticketYear + '%'
                GROUP BY 
                    TicketNumber
            )

            SELECT
                FORMAT(CAST(CreateDateTime AS DATE), 'MM-dd') AS CreateDate, 
                COUNT(t.TicketNumber) AS [TicketCount]
            FROM 
                app.CT_Tickets t
			JOIN
				min_id_cte ON min_id_cte.TicketNumber = t.TicketNumber AND min_id_cte.mID = t.id
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


### changed to query for department count on 10/3/2024 but left the return_operator verbage ###
def get_return_operator_counts(type, year):
    with coxn.connect() as connection:
        query = text("""
            SELECT 
                Department, 
                COUNT(Department)  AS [DepartmentCount]
            FROM 
                app.view_CT_Tickets 
            WHERE
                TicketType LIKE '%' + :ticketType + '%'
            AND
                TicketYear LIKE '%' + :ticketYear + '%'
            GROUP BY 
                Department;
        """)
        results = connection.execute(query, {'ticketType': type, 'ticketYear': year})

        roList = []
        countsList = []
        for row in results.all():
            roList.append(row[0])
            countsList.append(row[1])

        dict = {'ReturnOperatorCounts': {'ReturnOperators': roList, 'Counts': countsList}}

        return dict


### query for got it operator counts ###
def get_user_got_it_counts(type, year):
    with coxn.connect() as connection:
        query = text("""
            SELECT TOP 20
                u.Username, 
                ISNULL(g.GotItCount,0) AS GotItCount 
            FROM 
                app.CT_Users u
            LEFT JOIN 
                (SELECT 
                    GotItUser, 
                    COUNT(GotItUser) AS [GotItCount] 
                FROM 
                    app.view_CT_Tickets 
                WHERE
                    TicketType LIKE '%' + :ticketType + '%'
                AND
                    TicketYear LIKE '%' + :ticketYear + '%'
                GROUP BY 
                    GotItUser) g ON g.GotItUser = u.Username AND u.Username <> 'test'
            ORDER BY 
                g.GotItCount DESC,
                u.Username ASC;
        """)
        results = connection.execute(query, {'ticketType': type, 'ticketYear': year})

        usersList = []
        gotItCountsList = []
        for row in results.all():
            usersList.append(row[0])
            gotItCountsList.append(row[1])

        dict = {'UserGotItCounts': {'Usernames': usersList, 'GotItCounts': gotItCountsList}}

        return dict
