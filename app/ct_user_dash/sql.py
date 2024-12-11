from DBconnect import coxn
from sqlalchemy import text


def populate_user_dash_info(username):
    with coxn.connect() as connection:
        query = text("""
        SELECT 
            Username, 
            Email, 
            d.EmployeeDepartment 
        FROM 
            app.CT_Users u
        JOIN 
            app.CT_Departments d ON d.DeptID = u.DeptID
        WHERE 
            Username = :username;
	    """)
        results = connection.execute(query, {"username": username})

        user_info = {}
        for row in results.all():
            user_info.update(dict(row._mapping))

        return user_info


def populate_ticket_year_and_type_info():
    with coxn.connect() as connection:
        query = text("""
        SELECT 
            TicketType,
            TicketYear
        FROM 
            app.CT_TicketType
	    """)
        results = connection.execute(query)

        ticket_info = {}
        for row in results.all():
            ticket_info.update(dict(row._mapping))

        return ticket_info


def populate_tickets_created_count(username):
    with coxn.connect() as connection:
        query = text("""
            SELECT 
                COUNT(TicketNumber) AS TicketsCreatedCount
            FROM 
                app.view_CT_Tickets 
            WHERE 
                OriginalCreator = :username 
            AND 
                TicketType = (SELECT TicketType FROM app.CT_TicketType)
            AND
                TicketYear = (SELECT TicketYear FROM app.CT_TicketType);
    	    """)
        results = connection.execute(query, {"username": username})

        created_count = {}
        for row in results.all():
            created_count.update(dict(row._mapping))

        return created_count


def populate_tickets_worked_count(username):
    with coxn.connect() as connection:
        query = text("""
            SELECT 
                COUNT(DISTINCT t.TicketNumber) AS TicketsWorkedCount 
            FROM 
                app.CT_Tickets t
			LEFT JOIN
				app.CT_GotItTracking g ON g.TicketNumber = t.TicketNumber
            WHERE 
                t.TicketType = (SELECT TicketType FROM app.CT_TicketType)
            AND
                t.TicketYear = (SELECT TicketYear FROM app.CT_TicketType)
			AND
				( t.CreateUser = :username
			OR	
				g.GotItUser = :username
				);
    	    """)
        results = connection.execute(query, {"username": username})

        worked_count = {}
        for row in results.all():
            worked_count.update(dict(row._mapping))

        return worked_count


### user dashboard ticket query ###
def load_user_dash_ticket_history_from_db(username):
    with coxn.connect() as connection:
        query = text("""
        SELECT
            t.TicketNumber,
			t.ContactDate,
			t.ContactType,
			t.AccountNumber,
			t.ReturnOperator,
			t.Department,
			t.GotItUser,
			t.Status
        FROM 
            app.view_CT_Tickets t
		WHERE 
                t.TicketType = (SELECT TicketType FROM app.CT_TicketType)
            AND
                t.TicketYear = (SELECT TicketYear FROM app.CT_TicketType)
			AND
				( t.ReturnOperator = :username
			OR	
				t.GotItUser = :username
				)
        ORDER BY
            t.TicketNumber ASC;
        """)

        result = connection.execute(query, {"username": username})
        userTickets = []

        for row in result.all():
            userTickets.append(dict(row._mapping))

        return userTickets


### user dashboard ticket query ###
def load_dept_dash_ticket_history_from_db(dept):
    with coxn.connect() as connection:
        query = text("""
        SELECT
            t.TicketNumber,
			t.ContactDate,
			t.ContactType,
			t.AccountNumber,
			t.ReturnOperator,
			t.Department,
			t.GotItUser,
			t.Status
        FROM 
            app.view_CT_Tickets t
		WHERE 
                t.TicketType = (SELECT TicketType FROM app.CT_TicketType)
            AND
                t.TicketYear = (SELECT TicketYear FROM app.CT_TicketType)
			AND
				( t.ReturnOperator = :dept
			OR	
				t.GotItUser = :dept
			OR	
				t.Department = :dept
				)
        ORDER BY
            t.TicketNumber ASC;
        """)

        result = connection.execute(query, {"dept": dept})
        deptTickets = []

        for row in result.all():
            deptTickets.append(dict(row._mapping))

        return deptTickets


def populate_user_dash_chart(username):
    with coxn.connect() as connection:
        query = text("""
            ;WITH tickets_created_count AS
			(
			SELECT 
				OriginalCreator, 
				v.TicketType,
				v.TicketYear,
				COUNT(TicketNumber) AS TicketsCreatedCount
            FROM 
                app.view_CT_Tickets v
            WHERE 
                OriginalCreator = :username
			GROUP BY 
				OriginalCreator, TicketType, TicketYear
			)

			SELECT 
				--v.OriginalCreator AS Username, 
				v.TicketType,
				v.TicketYear,
				v.TicketsCreatedCount, 
				(t.TicketsWorkedCount - v.TicketsCreatedCount) AS TicketsWorkedCount 	
			FROM 
				tickets_created_count v
			CROSS APPLY
				(
				SELECT 
					COUNT(DISTINCT t.TicketNumber) AS TicketsWorkedCount 
				FROM 
					app.CT_Tickets t
				LEFT JOIN
					app.CT_GotItTracking g ON g.TicketNumber = t.TicketNumber
				WHERE 
					t.TicketYear = v.TicketYear
				AND 
					t.TicketType = v.TicketType
				AND
					( t.CreateUser = v.OriginalCreator
				OR	
					g.GotItUser = v.OriginalCreator
				)
			) t;
        """)

        result = connection.execute(query, {"username": username})
        userData = []

        for row in result.all():
            userData.append(dict(row._mapping))

        return userData