import os
from dotenv import load_dotenv
load_dotenv()
import jwt


def decodepasswordAdminHash(password):
    password = jwt.decode(password, os.getenv('adminHash'), algorithm="HS256")
    return password or ""


def decodepasswordUserHash(password):
    password = jwt.decode(password, os.getenv('UserHash'), algorithm="HS256")
    return password or ""
