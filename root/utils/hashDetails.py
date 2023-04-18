import os
from dotenv import load_dotenv
load_dotenv()
import jwt


def passwordAdminHash(password):
    password = jwt.encode({"password":password}, os.getenv('adminHash'), algorithm="HS256")
    return password


def passwordUserHash(password):
    password = jwt.encode({"password":password}, os.getenv('UserHash'), algorithm="HS256")
    return password


def getAdminToken(tokenString):
    password = jwt.encode({"token":tokenString}, os.getenv('adminTokenHash'), algorithm="HS256")
    return password

def getUserToken(tokenString):
    password = jwt.encode({"token":tokenString}, os.getenv('userTokenHash'), algorithm="HS256")
    return password