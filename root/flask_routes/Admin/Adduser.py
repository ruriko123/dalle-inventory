from flask import Blueprint,request
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file2 = Blueprint('app_file2',__name__)
from root.utils.converttoJson import listtojson
from root.utils.returnJson import successmsg,errormsg
from root.utils.hashDetails import passwordUserHash,getUserToken
from root.utils.getDate import getDateTime
from root.auth.check import checkAdmin


@app_file2.route("/addUser", methods=["POST"])
@cross_origin()
def addUser():
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
        if not "username" in json or json["username"]=="" or not "password" in json or json["password"]=="":
            data=errormsg("Required parameters not supplied.")
            cursor.close()
            mydb.close()
            return data,400
        username=json["username"]
        password=json["password"]
        checkUserNameExistsSQL=f"""select * from tblLogin where username=%s;"""
        cursor.execute(checkUserNameExistsSQL,(username,),)
        mydb.commit()
        result = cursor.fetchall()
        if result !=[]:
            data=errormsg("Username already taken.")
            return data,400
        else:
            currentDate=getDateTime()
            passwordhash = passwordUserHash(password)
            tokenstring = "{}{}".format(currentDate,password)
            token = getUserToken(tokenstring)
            insertAdminSQL=f"""INSERT INTO `tblLogin`(`username`, `password`,`token`,`type`) VALUES (%s,%s,%s,%s);"""
            cursor.execute(insertAdminSQL,(username,passwordhash,token,'USER',),)
            mydb.commit()
            data = {"token":str(token)}
            mydb.close()
            return data,200
    except Exception as error:
        data ={'error':str(error)}
        return data,400

