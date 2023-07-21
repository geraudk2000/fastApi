from jose import JWSError, jwt
from datetime import datetime, timedelta

#SECRET_KEY
#Algorithm 
#Exploration time


SECRET_KEY = "c77bd464e45d7bfc0ebaba5f3d5b85a6a78aeb1bf6986e76743270853540936f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt