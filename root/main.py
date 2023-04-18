from flask import Flask, Blueprint
app = Flask(__name__)
from flask_cors import CORS,cross_origin
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'secret!'
import os
from dotenv import load_dotenv
load_dotenv()
from root.models.createTables import *
createTables()


from root.flask_routes.Admin.insertItems import app_file1
from root.flask_routes.Admin.Adduser import app_file2
from root.flask_routes.Admin.AddAdmin import app_file3
from root.flask_routes.Login.login import app_file4
from root.flask_routes.Admin.getList.adminList import app_file5
from root.flask_routes.Admin.getList.userList import app_file6
from root.flask_routes.Admin.editUser.viewPassword import app_file7
from root.flask_routes.Admin.editUser.changeActive import app_file8




app.register_blueprint(app_file1)
app.register_blueprint(app_file2)
app.register_blueprint(app_file3)
app.register_blueprint(app_file4)
app.register_blueprint(app_file5)
app.register_blueprint(app_file6)
app.register_blueprint(app_file7)
app.register_blueprint(app_file8)


@app.route("/")
@cross_origin()
def index():
    return "working"



