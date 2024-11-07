from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sql as s
# Секретный ключ для подписи JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine("postgresql+psycopg2://stud:stud@db/archdb")


app = FastAPI()

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Модель данных для пользователя
class User(BaseModel):
    id: int = None
    username: str
    email: str
    password: str
    age: Optional[int] = None

# Модель данных для Посылки
class Package(BaseModel):
    id: int = None
    user_id: int
    height: float
    width: float
    long: float
    weight: float

# Временное хранилище для пользователей и товаров
users_db = []
package_db = []
order_db = []

# Псевдо-база данных пользователей (только для администратора)
client_db = {
    "admin": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # hashed "secret"
}

# Настройка паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Зависимости для получения текущего пользователя
async def get_current_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# Создание и проверка JWT токенов
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Маршрут для получения токена
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    password_check = False
    user = s.get_user(session, form_data.username)
    if user:
        password = form_data.password
        #print(f"\n{pwd_context.hash(password)}\n{user.password}")
        if pwd_context.verify(password, user.password):
            password_check = True

    if password_check:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        print(user.password)
        raise HTTPException(
            
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

# GET /users - Получить всех пользователей (требует аутентификации)
@app.get("/users", response_model=List[User])
def get_users(current_user: str = Depends(get_current_client)):
    return s.get_users_all(session)

# POST /users - Создать нового пользователя (требует аутентификации)
@app.post("/users", response_model=User)
def create_user(user: User, current_user: str = Depends(get_current_client)):
    try:
        return s.create_user(session, user.username, user.email, pwd_context.hash(user.password), user.age)
    except Exception as f:
        return f

# PUT /users/{user_id} - Обновить информацию о пользователе (требует аутентификации)
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User, current_user: str = Depends(get_current_client)):
    # for index, user in enumerate(users_db):
    #     if user.id == user_id:
    #         users_db[index] = updated_user
    #         return updated_user
    # raise HTTPException(status_code=404, detail="User not found")
    try:
        return s.update_user(session, user_id, updated_user.username, updated_user.email, pwd_context.hash(updated_user.password), updated_user.age)
    except Exception as f:
        return f

# GET /package - Получить список посылок (требует аутентификации)
@app.get("/package", response_model=List[Package])
def get_products(current_user: str = Depends(get_current_client)):
    return s.get_package(session)

# POST /products - Создать новую поссылку (требует аутентификации)
@app.post("/package", response_model=Package)
def create_product(package: Package, current_user: str = Depends(get_current_client)):
    try:
        return s.create_package(session, package.user_id, package.height, 
                                package.width, package.long, package.weight)
    except Exception as f:
        return f

# PUT /products/{package} - Обновить информацию о посылке (требует аутентификации)
@app.put("/package/{package}", response_model=Package)
def update_product(package: int, updated_product: Package, current_user: str = Depends(get_current_client)):
    try:
        return s.update_user(session, package, updated_product.user_id, updated_product.height, 
                                updated_product.width, updated_product.long, updated_product.weight)
    except Exception as f:
        return f

# Запуск сервера
# http://localhost:8000/openapi.json swagger
# http://localhost:8000/docs портал документации

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)