import os
from dotenv import load_dotenv
load_dotenv()
import jwt


def nameDecode(cName):
    cName = jwt.decode(cName, os.getenv('cNametoken'), algorithms=['HS256'])
    return cName["cName"]

def emailDecode(cEmail):
    cEmail= jwt.decode(cEmail, os.getenv('cEmailtoken'), algorithms=['HS256'])
    return cEmail["cEmail"]

def phoneDecode(cPhone):
    cPhone= jwt.decode(cPhone, os.getenv('cPhonetoken'), algorithms=['HS256'])
    return cPhone["cPhone"]

def addressDecode(cAddress):
    cAddress = jwt.decode(cAddress, os.getenv('cAddresstoken'), algorithms=['HS256'])
    return cAddress["cAddress"]

def ccDecode(ccardno):
    ccardno= jwt.decode(ccardno, os.getenv('cCardtoken'), algorithms=['HS256'])
    return ccardno["ccardno"]