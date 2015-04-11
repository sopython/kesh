from kesh.schema.base import fields, KeshSchema, convert


vote_schema_fields = {'Id': (fields.Integer, {'required':True}),
                           'PostId': (fields.Integer, {'required':True}),
                           'VoteTypeId': (fields.Integer, {'required':True}),
                           'UserId': (fields.Integer, {}),
                           'CreationDate': (fields.DateTime, {}),
                           'BountyAmount': (fields.Integer, {})
                          }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in vote_schema_fields.items()})

class VoteSchema(KeshSchema, mixin):
    pass


if __name__ == '__main__':
    s = r'''{"PostId" : "102",
             "VoteTypeId" : "101",
             "Id" : "-1",
             "UserId" : "3",
             "CreationDate" : "2008-08-26T00:16:53.810Z"}'''

    schema = VoteSchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')