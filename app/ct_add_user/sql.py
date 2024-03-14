from DBconnect import coxn
from sqlalchemy import text

def add_newuser_to_db(data, user):
    with coxn.connect() as connection:
        query = text("INSERT INTO dbo.CT_Users ( Username, Password, Department, Email, CreateUser) VALUES ( %s, %s, %s, %s, %s);"
                     % ( "'" + str(data['UserName']) + "'", "'" + str(data['Password']) + "'", "'" + str(data['Department']) + "'", "'" + str(data['Email']) + "'", "'" + str(user) + "'")
                     )
        #print(query)
        connection.execute(query)
        connection.commit()