import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

    

dbName = 'usuarios.slqite'
bade_dir = os.path.dirname(os.path.abspath(__file__))
dbUrl = f'sqlite:///{os.path.join(bade_dir, dbName)}'

engine = create_engine(dbUrl, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()