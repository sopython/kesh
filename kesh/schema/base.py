import re

from marshmallow import Schema, fields


class KeshSchema(Schema):
    pass


def convert(name):
   s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
   return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()