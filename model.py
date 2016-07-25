from sqlalchemy import (
    create_engine, String, Integer, Column, ForeignKey, DateTime, Boolean)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


#engine = create_engine('sqlite:///samples.db', echo=False)
engine = create_engine('postgresql+psycopg2://john@127.0.0.1/notes')

Base = declarative_base()


class Pattern(Base):
    __tablename__ = 'pattern'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    notes = Column(String)
    beats = Column(Integer)
    beat_unit = Column(Integer)


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
    bpm = Column(Integer)
    pattern_id = Column(Integer, ForeignKey('pattern.id'))
    deltas = relationship(
        "Delta", order_by=Delta.id, back_populates="attempt")
    extras = relationship(
        "Extra", order_by=Extra.id, back_populates="attempt")
    misses = relationship(
        "Miss", order_by=Miss.id, back_populates="attempt")
    result = Column(Boolean)
    created = Column(DateTime, server_default='now()')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
