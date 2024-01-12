# import Flask
from flask import Flask

# Inject Flask magic
app = Flask(__name__)

# Import routing to render the pages
from app.ct_create_ticket import routes
from app.ct_update_ticket import routes
from app.ct_home import routes