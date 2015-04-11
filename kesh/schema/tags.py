from kesh.schema.base import fields, KeshSchema, convert


tag_schema_fields = {'Id': (fields.Integer, {'required':True}),
                           'TagName': (fields.String, {'required':True}),
                           'Count': (fields.Integer, {'required':True}),
                           'ExcerptPostId': (fields.Integer, {}),
                           'WikiPostId': (fields.Integer, {})
                          }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in tag_schema_fields.items()})

class TagSchema(KeshSchema, mixin):
    pass


if __name__ == '__main__':
    s = r'''{"ExcerptPostId" : "102",
             "Count" : "101",
             "Id" : "-1",
             "WikiPostId" : "3",
             "TagName" : "Python"
}'''

    schema = TagSchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')