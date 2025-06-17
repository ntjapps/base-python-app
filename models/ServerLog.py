from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from database.config import openConnection

Base = declarative_base()


class ServerLogModel(Base):
    __tablename__ = 'log'

    id = db.Column(db.Uuid, primary_key=True)
    message = db.Column(db.String, nullable=False)
    channel = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    level_name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    context = db.Column(db.JSON, nullable=False)
    extra = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


def ServerLogSession():
    db = openConnection()
    Session = sessionmaker(bind=db)
    session = Session()
    return session
