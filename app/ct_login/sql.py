from DBconnect import coxn
from sqlalchemy import text

### user search for login ###
def user_login_search(username, password):
    with coxn.connect() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(DISTINCT Username) AS DoesExist FROM app.CT_Users WHERE Username LIKE :username AND Password LIKE :password;"), {'username': username, 'password': password}
        )

        login_results = result.all()[0]._mapping

        return (login_results['DoesExist'])


### check if user is Admin dept ###
def user_dept_check(username, dept1, dept2):
    with coxn.connect() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(DISTINCT Username) AS IsDept FROM app.CT_Users WHERE Username LIKE :username AND DeptID IN (:dept1, :dept2);"), {'username': username, 'dept1': dept1, 'dept2': dept2}
        )

        dept_results = result.all()[0]._mapping

        return (dept_results['IsDept'])