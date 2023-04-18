import os
from dotenv import load_dotenv
load_dotenv()
import jwt


def passwordHash(password):
    password = jwt.encode({"password":password}, os.getenv('adminHash'), algorithm="HS256")
    return password

def getAdminToken(tokenString):
    password = jwt.encode({"token":tokenString}, os.getenv('adminTokenHash'), algorithm="HS256")
    return password