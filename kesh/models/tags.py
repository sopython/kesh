from kesh.models.base import Base, Column, Integer, String
from kesh.models.base import ForeignKey

class Tag(Base):
    __tablename__ = 'tags'
    post_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    tag = Column(String, primary_key=True)

    def __repr__(self):
        return "<Tag(post_id={s.post_id}, tag={s.tag})>".format(s=self)