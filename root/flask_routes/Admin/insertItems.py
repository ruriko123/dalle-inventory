
from flask import Blueprint,request
from flask_cors import cross_origin
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
app_file1 = Blueprint('app_file1',__name__)
from root.utils.returnJson import successmsg


@app_file1.route("/insertItems", methods=["POST"])
@cross_origin()
def insertItems():
    try:
        mydb = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'))
        cursor = mydb.cursor(buffered=True)
        database_sql = "USE {};".format(os.getenv('database'))
        cursor.execute(database_sql)
        json = request.get_json()
        RequisitionDetailsList=json["RequisitionDetailsList"]
        for x in RequisitionDetailsList:
            itemid=x["ItemID"]
            checkItemexistsSQL=f"""SELECT * FROM `intbl_items` WHERE idIntbl_Items=%s"""
            cursor.execute(checkItemexistsSQL,(itemid,),)
            result = cursor.fetchall()
            if result ==[]:
                if x["ExpDate"]=="":
                    insertItemsSQL=f"""INSERT INTO `intbl_items`(`idIntbl_Items`, `Name`, `BrandName`, `Code`, `UOM`, `StockType`, `Department`, `GroupName`, `Status`, `Taxable`, `Rate`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(insertItemsSQL,(x["ItemID"],x["Name"],x["BrandName"],x["Code"],x["UOM"],x["StockType"],x["Department"],x["GroupName"],x["Status"],x["Taxable"],x["Rate"],),)
                    mydb.commit()
                else:
                    insertItemsSQL=f"""INSERT INTO `intbl_items`(`idIntbl_Items`, `Name`, `BrandName`, `Code`, `UOM`, `StockType`, `Department`, `GroupName`, `ExpDate`, `Status`, `Taxable`, `Rate`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(insertItemsSQL,(x["ItemID"],x["Name"],x["BrandName"],x["Code"],x["UOM"],x["StockType"],x["Department"],x["GroupName"],x["ExpDate"],x["Status"],x["Taxable"],x["Rate"],),)
                    mydb.commit()
            # else:
            # # insertItemsSQL=f"""INSERT INTO `intbl_items`(`idIntbl_Items`, `Name`, `BrandName`, `Code`, `UOM`, `StockType`, `Department`, `GroupName`, `ExpDate`, `Status`, `Taxable`, `Rate`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            # # cursor.execute(insertItemsSQL,(json["ItemID"],json["Name"],json["BrandName"],json["Code"],json["UOM"],json["StockType"],json["Department"],json["GroupName"],json["ExpDate"],json["Status"],json["Taxable"],json["Rate"],),)
            # # mydb.commit()
            # # mydb.close()
            #     data= errormsg("Entry with the itemID already exists.")
            #     return data,400  

        mydb.close()
        return successmsg("Success"), 200
    except Exception as error:
        data ={'error':str(error)}
        return data,400

       