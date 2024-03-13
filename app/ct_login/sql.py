from DBconnect import coxn
from sqlalchemy import text

### user search for login ###
def user_login_search(username, password):
    with coxn.connect() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(DISTINCT Username) AS DoesExist FROM dbo.CT_Users WHERE Username LIKE '{username}' AND Password LIKE '{password}';")
        )

        login_results = result.all()[0]._mapping

        return (login_results['DoesExist'])

