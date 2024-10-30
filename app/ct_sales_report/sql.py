from DBconnect import coxn
from sqlalchemy import text


### ticket search ###
def load_sales_from_db(beginDate, endDate):
    with coxn.connect() as connection:
        query = text(f"SELECT * FROM app.func_Sales_Report (:beginDate, :endDate) ORDER BY CAST(SaleDateFormatted AS DATE);")
        #print(query, values)
        results = connection.execute(query, {"beginDate": beginDate, "endDate": endDate})

        sales = []
        for row in results.all():
            sales.append(dict(row._mapping))
        return sales