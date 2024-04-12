# https://www.mssqltips.com/sqlservertip/7464/python-connect-to-sql-server/
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import DeclarativeBase
import urllib
from app import app

conn = urllib.parse.quote_plus(
    'Data Source Name=WebAppDataSource;'  # name of odbc connection created on server
    'Driver={ODBC Driver 17 for SQL Server};'
    f"Server={app.config['DB_SERVER_NAME']};"
    f"Database={app.config['DATABASE']};"
    'Trusted_connection=yes;'
    f"Username={app.config['USERNAME']};"
    f"Password={app.config['PASSWORD']};"
)

try:

    coxn = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn))
    print("Passed")

except:
    print("Failed!")

'''
class Base(DeclarativeBase):
    pass


class Users(Base):
    __table__ = Table('CT_Users', MetaData(), autoload_with=coxn, schema="app")

class Tickets(Base):
    __table__ = Table('CT_Tickets', MetaData(), autoload_with=coxn, schema="app")

class Accounts(Base):
    __table__ = Table('CT_Accounts', MetaData(), autoload_with=coxn, schema="app")

#print(Accounts.__table__.columns)
'''

'''
with coxn.connect() as connection:
    insert = connection.execute(Users.__table__.insert(),
                                {'Username': 'test', 'Password': '1234', 'Email': 'test@test.com',
                                 'Department': 'CS', 'CreateUser': 'test'})

    connection.commit()
    connection.close()
'''