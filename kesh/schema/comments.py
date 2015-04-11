from kesh.schema.base import fields, KeshSchema, convert

comment_schema_fields = {'Id': (fields.Integer, {'required':True}),
                        'PostId': (fields.Integer, {'required':True}),
                        'CreationDate': (fields.DateTime, {}),
                        'Text': (fields.String, {'required':True}),
                        'Location': (fields.String, {}),
                        'Score': (fields.Integer, {}),
                        'UserId': (fields.Integer, {}),
                        'UserDisplayName': (fields.String, {})
                     }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in comment_schema_fields.items()})

class CommentSchema(KeshSchema, mixin):
    pass


if __name__ == '__main__':
    s = r'''{"PostId" : "102",
             "Text" : "101",
             "Id" : "-1",
             "UserId" : "3",
             "CreationDate" : "2008-08-26T00:16:53.810Z"}'''

    schema = CommentSchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')