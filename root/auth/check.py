import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()




def checkAdmin(token):
    try:
        mydb = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'))
        cursor = mydb.cursor(buffered=True)
        database_sql = "USE {};".format(os.getenv('database'))
        cursor.execute(database_sql)
        get_outlet_sql = """select ID from tblLogin where token=%s and isActive=%s and type='ADMIN'"""
        cursor.execute(get_outlet_sql,(token,True,),)
        result = cursor.fetchall()
        if result == []:
            return False

        return True
    except Exception as error:
        return False

def checkUser(token):
    try:
        mydb = mysql.connector.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'))
        cursor = mydb.cursor(buffered=True)
        database_sql = "USE {};".format(os.getenv('database'))
        cursor.execute(database_sql)
        get_outlet_sql = """select ID from tblLogin where token=%s and isActive=%s and type='USER'"""
        cursor.execute(get_outlet_sql,(token,True,),)
        result = cursor.fetchall()
        if result == []:
            return False

        return True
    except Exception as error:
        return False