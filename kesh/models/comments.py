from kesh.models.base import Base, Column, DateTime, Integer, String, Text
from kesh.models.base import relationship, ForeignKey, sessionmaker, create_engine
from kesh.models.base import declared_attr
from kesh.models.users import User

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))

    score = Column(Integer)

    text = Column(Text)

    creation_date = Column(DateTime)

    user_id = Column(Integer)
    user_display_name = Column(String)

    def __repr__(self):
        return "<Comment>(id={s.id})".format(s=self)