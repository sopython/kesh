from kesh.models.base import Base, Column, DateTime, Integer, String, Text
from kesh.models.base import relationship, ForeignKey, sessionmaker, create_engine
from kesh.models.comments import Comment
from kesh.models.tags import Tag
from kesh.models.users import User

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)

    post_type_id = Column(Integer)

    creation_date = Column(DateTime)

    score = Column(Integer)
    view_count = Column(Integer)

    body = Column(Text)

    owner_user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User')

    last_editor_user_id = Column(Integer)
    last_editor_display_name = Column(String)
    last_edit_date = Column(DateTime)

    last_activity_date = Column(DateTime)
    community_owned_date = Column(DateTime)

    comment_count = Column(Integer)

    title = Column(String)

    tags = relationship('Tag')

    answer_count = Column(Integer)
    favorite_count = Column(Integer)

    accepted_answer_id = Column(Integer)

    closed_date = Column(DateTime)

    # Used if the post is an answer and so has a parent question.
    parent_id = Column(String, ForeignKey('posts.id'))
    parent_question = relationship('Post', remote_side=[id])

    # Used if the post is a question and so may have multiple answers.
    answers = relationship('Post')

    comments = relationship('Comment')

    def __repr__(self):
        return "<Post>(id={s.id}, type=s.post_type_id)".format(s=self)


if __name__ == '__main__':

    engine = create_engine('sqlite:///:memory:', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    q = Post(id=123, post_type_id=1, owner_user_id=3005188)
    a = Post(id=1, post_type_id=2, parent_id=123, owner_user_id=3005188)
    u = User(id=3005188, display_name='Ffisegydd')
    c = Comment(id=1, user_id=3005188, post_id=1)
    tags = [Tag(post_id=123, tag='python'), Tag(post_id=123, tag='pandas')]

    session.add_all([q, a, u, c])
    session.add_all(tags)

    a = session.query(Post).filter(Post.id == 1).one()
    q = a.parent_question

    print('\n', q, a, q.answers, q.answers[0].comments, sep='\n\n')

