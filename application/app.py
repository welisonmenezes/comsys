from flask import Flask, render_template, redirect, url_for

# create a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# apply app configurations
app.config.from_pyfile('config.py')

from Modules import *

app.register_blueprint(DashboardController)

@app.route('/')
def index():
    return 'hello world'

if __name__ == "__main__":
    app.run()