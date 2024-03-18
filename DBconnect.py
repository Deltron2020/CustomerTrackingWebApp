# https://www.mssqltips.com/sqlservertip/7464/python-connect-to-sql-server/
import sqlalchemy as sa
from sqlalchemy import create_engine
import urllib
import pyodbc

conn = urllib.parse.quote_plus(
    'Data Source Name=WebAppDataSource;'
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=APWT-PatriotSQL;'
    'Database=MartinTraining;'
    'Trusted_connection=yes;'
)

try:

    coxn = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn))
    print("Passed")

except:
    print("failed!")