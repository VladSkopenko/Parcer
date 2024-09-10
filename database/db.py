from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from database.conf import config
engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
