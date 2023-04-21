from flask import Blueprint,request
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file9 = Blueprint('app_file9',__name__)
from root.utils.returnJson import errormsg
from root.utils.hashDetails import passwordUserHash,getUserToken
from root.utils.getDate import getDateTime
from root.auth.check import checkUser


@app_file9.route("/franchiseorder", methods=["POST"])
@cross_origin()
def franchiseorder():
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
        if not checkUser(json["token"]):
            data = errormsg("Not allowed.")
            return data,401

        Date=json["Date"]
        Department=json["Department"]
        Type=json["Type"]
        Origin=json["Origin"]
        DestinationStore=json["DestinationStore"]
        State=json["State"]
        receivedDate=json["receivedDate"]

        insertorderSQL=f"""INSERT INTO `intblstorerequisition` ( `Date`, `Department`, `Type`, `Origin`, `DestinationStore`, `State`, `receivedDate`) VALUES ( %s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(insertorderSQL,(Date,Department,Type,Origin,DestinationStore,State,receivedDate,),)
        mydb.commit()



        primarykey=cursor.lastrowid
        for x in json["intblstorereqdetails"]:
            checkUserNameExistsSQL=f"""INSERT INTO `dalleinventory`.`intblstorereqdetails` ( `ItemID`, `StoreReqID`, `Amount`, `UOM`, `Rate`) VALUES ( %s %s, %s, %s, %s);"""
            cursor.execute(checkUserNameExistsSQL,(x["ItemID"],primarykey,["Amount"],x["UOM"],x["Rate"],),)
            mydb.commit()
        data = {"token":str()}
        mydb.close()
        return data,200
    except Exception as error:
        data ={'error':str(error)}
        return data,400

