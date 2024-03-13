# import Flask
from flask import Flask, session

# Inject Flask magic
app = Flask(__name__)
app.secret_key = "Sailfish1"

# Import routing to render the pages
from app.ct_create_ticket import routes
from app.ct_update_ticket import routes
from app.ct_home import routes
from app.ct_login import routes