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


### query for tickets by Return Operator Dept ###
def get_return_operator_counts(type, year):
    with coxn.connect() as connection:
        query = text("""
        ;WITH dept_counts_cte AS
        (
        SELECT
            TicketNumber,
            IIF(ReturnOperator IN (SELECT EmployeeDepartment FROM app.CT_Departments), ReturnOperator, ud.EmployeeDepartment) AS [ReturnOperator]
        FROM
            app.view_CT_Tickets t
        LEFT JOIN
        (
            SELECT UserName, d.EmployeeDepartment FROM app.CT_Users u
            JOIN app.CT_Departments d ON d.DeptID = u.DeptID
        ) ud ON ud.Username = t.ReturnOperator
        WHERE
				TicketType LIKE '%' + :ticketType + '%'
		AND
				TicketYear LIKE '%' + :ticketYear + '%'
        )
        
        SELECT
            ReturnOperator,
            COUNT(TicketNumber) AS [DeptCount]
        FROM
            dept_counts_cte
        WHERE 
            ReturnOperator IS NOT NULL
        GROUP BY 
            ReturnOperator;
        """)
        results = connection.execute(query, {'ticketType': type, 'ticketYear': year})

        roList = []
        countsList = []
        for row in results.all():
            roList.append(row[0])
            countsList.append(row[1])

        dict = {'ReturnOperatorCounts': {'ReturnOperators': roList, 'Counts': countsList}}

        return dict
