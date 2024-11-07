from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer)
    
# Определение модели пакета
class Package(Base):
    __tablename__ = 'packages'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

def get_user(session : sessionmaker, username:str) -> User:
    return session.query(User).filter(User.username == username).first()

def get_users_all(session : sessionmaker) -> User:
    return session.query(User).all()

def create_user(session : sessionmaker, 
                username: str, email: str, 
                password: str, age: int):
        # Create a new User instance
    new_user = User(
        username=username,
        email=email,
        password=password,
        age=age
    )
    
    # Add the new user to the session
    session.add(new_user)
    
    # Commit the session to save the user to the database
    session.commit()
    
    # Optionally return the created user
    return new_user

def update_user(session: sessionmaker, user_id: int, 
                username: str = None, email: str = None, 
                password: str = None, age: int = None):
    # Найти пользователя по id
    user = session.query(User).filter(User.id == user_id).first()
    
    # Проверка, существует ли пользователь
    if user is None:
        print("Пользователь не найден.")
        return None
    
    # Обновление полей, если они переданы
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if password is not None:
        user.password = password
    if age is not None:
        user.age = age
    
    # Коммит изменений в сессии
    session.commit()
    
    # Возвращаем обновленного пользователя
    return user

def get_package(session: sessionmaker, package_id: int) -> Package:
    """Получить пакет по его ID."""
    return session.query(Package).filter(Package.id == package_id).first()

def get_packages_all(session: sessionmaker) -> list[Package]:
    """Получить все пакеты."""
    return session.query(Package).all()

def create_package(session: sessionmaker, user_id: int, height: float, 
                   width: float, long: float, weight: float) -> Package:
    """Создать новый пакет."""
    new_package = Package(
        user_id=user_id,
        height=height,
        width=width,
        long=long,
        weight=weight
    )
    
    session.add(new_package)
    session.commit()
    
    return new_package

def update_package(session: sessionmaker, package_id: int, 
                   height: float = None, width: float = None, 
                   long: float = None, weight: float = None) -> Package:
    """Обновить пакет по его ID."""
    package = session.query(Package).filter(Package.id == package_id).first()
    
    if package is None:
        print("Пакет не найден.")
        return None
    
    if height is not None:
        package.height = height
    if width is not None:
        package.width = width
    if long is not None:
        package.long = long
    if weight is not None:
        package.weight = weight
    
    session.commit()
    
    return package
