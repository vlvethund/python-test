import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def connectdb():
    load_dotenv()
    db_url = os.environ.get('db_url')
    engine = create_engine(f'mysql+pymysql://{db_url}')
    return get_session(engine)


def get_session(engine):
    session = sessionmaker()
    session.configure(bind=engine)

    return session()


if __name__ == '__main__':
    sqlalchemy_session = connectdb()
    print(sqlalchemy_session)
