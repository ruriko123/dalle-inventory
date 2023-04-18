from flask import  Blueprint,request
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file8 = Blueprint('app_file8',__name__)
from root.utils.returnJson import successmsg,errormsg
from root.auth.check import checkAdmin

@app_file8.route("/changeActive", methods=["POST"])
@cross_origin()
def viewPassword():
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
        if not "username" in json or json["username"]=="" or not "id" in json or json["id"]=="":
            data=errormsg("Required parameters not supplied.")
            cursor.close()
            mydb.close()
            return data,400
        if json["username"]==os.getenv('ADMIN_USERNAME'):
            data=errormsg("Cannot perform this action on default admin.")
            mydb.close()
            return data,400

        else:
            userid=json["id"]
            username=json["username"]
            changeActiveSQL=f"""INSERT INTO `tblLogin`(`ID`, `username`) VALUES (%s,%s) on DUPLICATE key update isActive= if(isActive,False,True)"""
            cursor.execute(changeActiveSQL,(userid,username,),)
            mydb.commit()
            mydb.close()
            data=successmsg("Changed status")
            return data,400
    except Exception as error:
        data ={'error':str(error)}
        return data,400