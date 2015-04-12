from kesh.models.base import Base, Column, DateTime, Integer, String, Text
from kesh.models.base import relationship, ForeignKey, sessionmaker, create_engine
from kesh.models.tags import Tag

class Post():
    id = Column(Integer, primary_key=True)

    creation_date = Column(DateTime)

    score = Column(Integer)
    view_count = Column(Integer)

    body = Column(Text)

    owner_user_id = Column(Integer)
    owner_user_display_name = Column(String)

    last_editor_user_id = Column(Integer)
    last_editor_display_name = Column(String)
    last_edit_date = Column(DateTime)

    last_activity_date = Column(DateTime)

    comment_count = Column(Integer)

    community_owned_date = Column(DateTime)


class Question(Base, Post):
    __tablename__ = 'questions'

    title = Column(String)

    tags = relationship('Tag')

    answer_count = Column(Integer)
    favorite_count = Column(Integer)

    accepted_answer_id = Column(Integer)

    closed_date = Column(DateTime)

    def __repr__(self):
        return "<Question>(id={s.id})".format(s=self)


class Answer(Base, Post):
    __tablename__ = 'answers'

    parent_id = Column(String, ForeignKey('questions.id'))

    parent = relationship('Question')

    def __repr__(self):
        return "<Answer>(id={s.id})".format(s=self)

if __name__ == '__main__':

    engine = create_engine('sqlite:///:memory:', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    q = Question(id=123)
    a = Answer(id=1, parent_id=123)
    tags = [Tag(post_id=123, tag='python'), Tag(post_id=123, tag='pandas')]

    session.add_all([q, a])
    session.add_all(tags)

    a = session.query(Answer).one()
    q = a.parent

    print(q, a, q.tags, sep='\n\n')

