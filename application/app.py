from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS

# TODO: create a global location where Exceptions are processed

# create application
app = Flask(__name__, template_folder='Views/UI', static_folder='Views/UI/static')
app.config.from_pyfile('config.py')
app_config = app.config

# configurate logging
if app_config['ENABLE_LOG_FILE']:
    from Utils import Logger
    Logger(app)

# create api blueprint
ApiBP = Blueprint('ApiBP', __name__, url_prefix='/api')
cors = CORS(ApiBP, resources={r"/api/*": {"origins": "*"}})
api = Api(ApiBP)
app.register_blueprint(ApiBP)

# start controllers
from Controllers import start_controllers
start_controllers(app, api)

# start views
from Views import start_view
start_view(app)

#from Models import Engine, Base
#Base.metadata.drop_all(Engine)
#Base.metadata.create_all(Engine)

if __name__ == "__main__":
    app.run()