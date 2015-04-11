from kesh.schema.base import fields, KeshSchema, convert

user_schema_fields = {'Id': (fields.Integer, {'required':True}),
                      'Reputation': (fields.Integer, {}),
                      'CreationDate': (fields.DateTime, {}),
                      'DisplayName': (fields.String, {}),
                      'LastAccessDate': (fields.DateTime, {}),
                      'WebsiteUrl': (fields.Url, {}),
                      'Location': (fields.String, {}),
                      'AboutMe': (fields.String, {}),
                      'Views': (fields.Integer, {}),
                      'UpVotes': (fields.Integer, {}),
                      'DownVotes': (fields.Integer, {}),
                      'AccountId': (fields.Integer, {}),
                      'Age': (fields.Integer, {})
                     }

mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in user_schema_fields.items()})

class UserSchema(KeshSchema, mixin):
    pass

if __name__ == '__main__':
    s = r'''{"AccountId" : "-1",
        "AboutMe" : "<p>Hi, I'm not really a person.</p>\n\n<p>I'm a background process that helps keep this site clean!</p>\n\n<p>I do things like</p>\n\n<ul>\n<li>Randomly poke old unanswered questions every hour so they get some attention</li>\n<li>Own community questions and answers so nobody gets unnecessary reputation from them</li>\n<li>Own downvotes on spam/evil posts that get permanently deleted</li>\n<li>Own suggested edits from anonymous users</li>\n<li><a href=\"http://meta.stackexchange.com/a/92006\">Remove abandoned questions</a></li>\n</ul>\n",
        "Id" : "-1",
        "Location" : "on the server farm",
        "CreationDate" : "2008-07-31T00:00:00Z",
        "UpVotes" : "102041",
        "DisplayName" : "Community",
        "WebsiteUrl" : "http://meta.stackexchange.com/",
        "Views" : "649",
        "DownVotes" : "441996",
        "LastAccessDate" : "2008-08-26T00:16:53.810Z",
        "Reputation" : "1"
}'''

    schema = UserSchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')