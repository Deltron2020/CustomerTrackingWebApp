# import Flask
from flask import Flask, render_template
import logging
from logging.handlers import RotatingFileHandler
import json

# Inject Flask magic
app = Flask(__name__, instance_relative_config=True)
app.config.update(
        USERNAME=None,
        PASSWORD=None,
        DB_SERVER_NAME=None,
        DATABASE=None
)
app.config.from_file('credentials.json', load=json.load)

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    file_handler = RotatingFileHandler('C:\inetpub\wwwroot\logs.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
    return render_template('500.html'), 500

# Import routing to render the pages
from app.ct_create_ticket import routes
from app.ct_update_ticket import routes
from app.ct_home import routes
from app.ct_login import routes
from app.ct_add_user import routes
from app.ct_dashboard import routes
from app.ct_account_history import routes
