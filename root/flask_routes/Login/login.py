
from flask import Flask, Blueprint,request,jsonify
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file4 = Blueprint('app_file4',__name__)
from root.utils.converttoJson import listtojson
from root.utils.returnJson import successmsg,errormsg
from root.utils.hashDetails import passwordAdminHash,passwordUserHash

@app_file4.route("/login", methods=["POST"])
@cross_origin()
def login():
    try:
        mydb = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'))
        cursor = mydb.cursor(buffered=True)
        database_sql = "USE {};".format(os.getenv('database'))
        cursor.execute(database_sql)
        json = request.get_json()

        if not "type" in json or json["type"]=="" or not "username" in json or json["username"]=="" or not "password" in json or json["password"]=="":
            data=errormsg("Required parameters not supplied.")
            cursor.close()
            mydb.close()
            return data,400
        username=json["username"]
        password=json["password"]
        userType=json["type"]
        if not userType=="ADMIN" and not userType=="USER":
            data=errormsg("User type not supplied")
            mydb.close()
            return data,400
        if userType=="ADMIN":
            passwordhash = passwordAdminHash(password)
        else:
            passwordhash = passwordUserHash(password)

        checkUserNameExistsSQL=f"""select * from tblLogin where username=%s and password=%s and isActive=%s;"""
        cursor.execute(checkUserNameExistsSQL,(username,passwordhash,True,),)
        mydb.commit()
        result = cursor.fetchall()
        if result ==[]:
            data=errormsg("Incorrect Username or Password.")
            return data,400
        else:
            getUserDetailsSQL=f"""SELECT `token`, `type` FROM `tblLogin` WHERE username=%s and password=%s"""
            cursor.execute(getUserDetailsSQL,(username,passwordhash,),)
            mydb.commit()
            result=cursor.fetchall()
            jsonData=listtojson(result,cursor.description)
            data = {"success":jsonData[0]}
            mydb.close()
            return data,200
    except Exception as error:
        data ={'error':str(error)}
        return data,400

