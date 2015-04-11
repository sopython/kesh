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