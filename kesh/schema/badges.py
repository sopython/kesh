from kesh.schema.base import fields, KeshSchema, convert


badge_schema_fields = {'Id': (fields.Integer, {'required':True}),
                       'Date': (fields.DateTime, {}),
                       'Name': (fields.String, {'required':True}),
                       'UserId': (fields.Integer, {}),
                      }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in badge_schema_fields.items()})

class BadgeSchema(KeshSchema, mixin):
    pass


if __name__ == '__main__':
    s = r'''{"Name" : "Sheriff",
             "Id" : "-1",
             "UserId" : "3",
             "Date" : "2008-08-26T00:16:53.810Z"}'''

    schema = BadgeSchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')