# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
# from fastapi import Depends #type: ignore
# from typing import Annotated
# import os
# from dotenv import load_dotenv

# load_dotenv()

# cloud_db = os.environ["DATABASE_URL"]





# engine = create_engine(
#     cloud_db,
#     echo=True
# )

# sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# class Base(DeclarativeBase):
#     pass

# def get_db():
#     db = sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from fastapi import Depends
from typing import Annotated
import os
from helpers.config import cloud_db

engine = create_engine(
    cloud_db,
    echo=True
)

# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# db_dependency = Annotated[AsyncSession, Depends(get_db)]
db_dependency = Annotated[Session, Depends(get_db)]