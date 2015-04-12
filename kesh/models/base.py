from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()