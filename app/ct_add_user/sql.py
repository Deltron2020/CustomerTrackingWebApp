from DBconnect import coxn
from sqlalchemy import text

def add_newuser_to_db(data, user):
    with coxn.connect() as connection:
        query = text(f"INSERT INTO app.CT_Users ( Username, Password, Department, Email, CreateUser) VALUES ( '{data['UserName']}', '{data['Password']}', '{data['Department']}', '{data['Email']}', '{user}');"
                     )
        #print(query)
        connection.execute(query)
        connection.commit()