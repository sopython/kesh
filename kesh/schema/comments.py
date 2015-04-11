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