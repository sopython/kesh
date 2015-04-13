from kesh.models.base import Base, Column, DateTime, Integer, String, Text
from kesh.models.base import relationship, ForeignKey, sessionmaker, create_engine
from kesh.models.tags import Tag

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    display_name = Column(String)
    se_account_id = Column(Integer)

    reputation = Column(Integer)
    creation_date = Column(DateTime)

    last_access_date = Column(DateTime)

    website_url = Column(String)
    location = Column(String)
    about_me = Column(Text)
    views = Column(Integer)

    up_votes = Column(Integer)
    down_votes = Column(Integer)

    age = Column(Integer)

    def __repr__(self):
        return "<User(id={s.id}, name={s.display_name})>".format(s=self)