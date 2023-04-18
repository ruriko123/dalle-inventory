from flask import Flask, Blueprint,request,jsonify
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file7 = Blueprint('app_file7',__name__)
from root.utils.converttoJson import listtojson
from root.utils.returnJson import successmsg,errormsg
from root.utils.decodeDetails import decodepasswordAdminHash,decodepasswordUserHash
from root.auth.check import checkAdmin

@app_file7.route("/viewPassword", methods=["POST"])
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

        else:
            userid=json["id"]
            username=json["username"]
            insertAdminSQL=f"""select password,type from tblLogin where username=%s and ID=%s;"""
            cursor.execute(insertAdminSQL,(username,userid,),)
            mydb.commit()
            result = cursor.fetchall()
            jsondata = listtojson(result,cursor.description)
            usertype = jsondata[0]["type"]
            password = jsondata[0]["password"]
            if usertype=="ADMIN":
                userpass = decodepasswordAdminHash(password)
                if userpass=="":
                    data=errormsg("Error while decoding password")
                    return data,400
                data={"password":str(userpass)}
                mydb.close()
                return data,200
            elif usertype=="USER":
                userpass = decodepasswordUserHash(password)
                if userpass=="":
                    data=errormsg("Error while decoding password")
                    return data,400
                data={"password":str(userpass)}
                mydb.close()
                return data,200
            data=errormsg("Error")
            mydb.close()
            return data,400
    except Exception as error:
        data ={'error':str(error)}
        return data,400