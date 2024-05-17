# https://www.mssqltips.com/sqlservertip/7464/python-connect-to-sql-server/
from sqlalchemy import create_engine
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
