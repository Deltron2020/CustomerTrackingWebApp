# import Flask
from flask import Flask, session
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


# Import routing to render the pages
from app.ct_create_ticket import routes
from app.ct_update_ticket import routes
from app.ct_home import routes
from app.ct_login import routes
from app.ct_add_user import routes
