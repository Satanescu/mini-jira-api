import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #we use this to "prepare" a password for hasing of for verifying it s a Toolbox that let s us work with passwords

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) #used for the login to verify the password that the user enters to the one in the DB

def get_password_hash(password):
    return pwd_context.hash(password) #used for registration to hash the password

def create_access_token(data: dict): #data is the dictionary that we recive "user": "Raul"
    to_encode = data.copy() #copy the dictionary to keep the data from the original one intact
    expire =datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # calculates the time of the moment when the token expire " now + ACCESS_TOKEN_EXPIRE_MINUTES"

    to_encode.update({"exp": expire}) #this adds the expiration time to the dictionary

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # this mixes up the data just created with the secret key and the alghoritm
    return encoded_jwt