from sqlalchemy import (
    create_engine, String, Integer, Column, ForeignKey)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///samples.db', echo=False)
Base = declarative_base()


class Delta(Base):
    __tablename__ = 'delta'
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey('attempt.id'))
    ts = Column(Integer)
    val = Column(Integer)
    attempt = relationship("Attempt", back_populates='deltas')


class Miss(Base):
    __tablename__ = 'miss'
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey('attempt.id'))
    ts = Column(Integer)
    attempt = relationship("Attempt", back_populates='misses')


class Extra(Base):
    __tablename__ = 'extra'
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey('attempt.id'))
    ts = Column(Integer)
    attempt = relationship("Attempt", back_populates='extras')

    
class Attempt(Base):
    __tablename__ = 'attempt'
    id = Column(Integer, primary_key=True)
    deltas = relationship(
        "Delta", order_by=Delta.id, back_populates="attempt")
    extras = relationship(
        "Extra", order_by=Extra.id, back_populates="attempt")
    misses = relationship(
        "Miss", order_by=Miss.id, back_populates="attempt")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
