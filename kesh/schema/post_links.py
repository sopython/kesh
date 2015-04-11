from kesh.schema.base import fields, KeshSchema, convert

post_link_type_id = {1: 'Linked',
                     3: 'Duplicate'}

post_link_schema_fields = {'Id': (fields.Integer, {'required':True}),
                           'CreationDate': (fields.DateTime, {'required':True}),
                           'PostId': (fields.Integer, {'required':True}),
                           'RelatedPostId': (fields.Integer, {'required':True}),
                           'LinkTypeId': (fields.Integer, {'required':True})
                          }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in post_link_schema_fields.items()})

class PostLinkSchema(KeshSchema, mixin):
    pass
@PostLinkSchema.preprocessor
def add_post_link_string(schema, input_data):
    try:
        input_data['link_type_string'] = post_link_type_id[input_data['link_type_id']]
    except KeyError:
        pass
    return input_data

if __name__ == '__main__':
    s = r'''{"RelatedPostId" : "102",
             "PostId" : "101",
             "Id" : "-1",
             "CreationDate" : "2008-07-31T00:00:00Z",
             "LinkTypeId" : "3"
}'''

    schema = PostLinkSchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')