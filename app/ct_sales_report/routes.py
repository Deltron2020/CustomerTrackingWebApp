from flask import render_template, request, session, redirect, url_for
import json
from app.ct_sales_report.sql import (load_sales_from_db)
from app import app


@app.route("/sales_report")
def customer_tracking_sales_report():
    return render_template('CT_SalesReport.html')



# json search functionality
@app.route("/sales_report_json", methods=['GET'])
def customer_tracking_sales_report_json():
    try:
        if 'username' in session:
            data = request.args

            results = load_sales_from_db(beginDate=data['begin'], endDate=data['end'])

            json_data = json.dumps(results, indent=4, sort_keys=True, default=str)
            #print(json_data)

            return json_data

        else:
            return redirect(url_for('customer_tracking_login'))
    except Exception as e:
        return render_template('CT_Error.html', error=e)