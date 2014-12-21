from .post import Post

class Question(Post):

    def __init__(self, db):
        super().__init__(db=db)


    def get_question_by_id(self, id):
        d = {'collection':'questions', 'id':id}

        result = self.db.query(d)

        return result