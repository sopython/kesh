from kesh.schema.base import fields, KeshSchema, convert


post_schema_fields = {'Id': (fields.Integer, {'required':True}),
                      'PostTypeId': (fields.Integer, {'required':True}),
                      'CreationDate': (fields.DateTime, {'required':True}),
                      'Score': (fields.Integer, {'required':True}),
                      'ViewCount': (fields.Integer, {'required':True}),
                      'Body': (fields.String, {'required':True}),
                      'OwnerUserId': (fields.Integer, {}),
                      'OwnerUserDisplayName': (fields.Integer, {}),
                      'LastEditorUserId': (fields.Integer, {}),
                      'LastEditorDisplayName': (fields.String, {}),
                      'LastEditDate': (fields.DateTime, {}),
                      'LastActivityDate': (fields.DateTime, {}),
                      'CommentCount': (fields.Integer, {'required':True}),
                      'CommunityOwnedDate': (fields.DateTime, {})
                     }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in post_schema_fields.items()})

class PostSchema(KeshSchema, mixin):
    pass


question_schema_fields = {'Title': (fields.String, {'required':True}),
                          'Tags': (fields.String, {'required':True}),
                          'AnswerCount': (fields.Integer, {'required':True}),
                          'FavoriteCount': (fields.Integer, {'required':True}),
                          'AcceptedAnswerId': (fields.Integer, {}),
                          'ClosedDate': (fields.DateTime, {})
                         }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in question_schema_fields.items()})

class QuestionSchema(PostSchema, mixin):
    pass
@QuestionSchema.preprocessor
def convert_tag_string_to_list(schema, input_data):
    input_data['tags'] = [i.strip('<') for i in input_data['tags'].split('>')[:-1]]
    return input_data


answer_schema_fields = {'ParentId': (fields.Integer, {'required':True})}
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in answer_schema_fields.items()})

class AnswerSchema(PostSchema, mixin):
    pass


if __name__ == '__main__':
    s = '''{"Id":"12345", "PostTypeId":"1", "CreationDate":"2012-04-21T18:25:43","Score":"10", "ViewCount":"120",
    "Body":"Hello! My name is Keiron!", "Title":"Question!", "Tags":"<python><pandas><numpy>", "AnswerCount":"0",
    "CommentCount":"20", "FavoriteCount":"12000"}'''
    d = {"Id":"12345", "PostTypeId":"1", "CreationDate":"2012-04-21T18:25:43","Score":"10", "ViewCount":"120",
    "Body":"Hello! My name is Keiron!", "Title":"Question!", "Tags":"<python><pandas><numpy>", "AnswerCount":"0",
    "CommentCount":"20", "FavoriteCount":"12000"}

    schema = QuestionSchema()

    data, errors = schema.load(dict(d.items()))

    print(data, errors, sep='\n\n\n')
