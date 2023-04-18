from flask import Flask, Blueprint,request,jsonify
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file5 = Blueprint('app_file5',__name__)
from root.utils.converttoJson import listtojson
from root.utils.returnJson import successmsg,errormsg
from root.utils.hashDetails import passwordAdminHash
from root.utils.getDate import getDateTime
from root.auth.check import checkAdmin

@app_file5.route("/AdminList", methods=["POST"])
@cross_origin()
def AdminList():
    try:
        mydb = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'))
        cursor = mydb.cursor(buffered=True)
        database_sql = "USE {};".format(os.getenv('database'))
        cursor.execute(database_sql)
        json = request.get_json()
        if "token" not in json or json["token"]=="":
            data=errormsg("Token not provided.")
            mydb.close()
            return data,401
        if not checkAdmin(json["token"]):
            data = errormsg("Not allowed.")
            return data,401
        else:
            insertAdminSQL=f"""select ID,username from tblLogin where type='ADMIN' GROUP by ID;"""
            cursor.execute(insertAdminSQL)
            mydb.commit()
            result = cursor.fetchall()
            jsondata = listtojson(result,cursor.description)
            data = {"details":jsondata}
            mydb.close()
            return data,200
    except Exception as error:
        data ={'error':str(error)}
        return data,400