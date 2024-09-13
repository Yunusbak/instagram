import os
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
load_dotenv()


ENGINE = create_engine(
    f'{os.getenv('db_app')}://'
    f'{os.getenv('db_user')}:'
    f'{os.getenv('db_password')}'
    f'@{os.getenv('db_host')}/'
    f'{os.getenv('db_name')}',
    echo=True
)
Base = declarative_base()
Session = sessionmaker()
