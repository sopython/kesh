from pymongo import MongoClient
from lxml import etree

from time import gmtime, strftime
import os
import re

data_dir = '../../../bin/so_data_/'
file_name = 'Tags.xml'
db_name = 'kesh'
coll_name = 'tags'

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Id', 'Count', 'ExcerptPostId', 'WikiPostId'}

def convert(name):
   s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
   return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

f = open(os.path.join(data_dir, './logs/{:s}.log'.format(coll_name)), 'w')
f.write('Importing {:s} data.\n\n'.format(coll_name))

for i, (event, elem) in enumerate(context):
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = {convert(k):int(v) if k in str_to_int else
             v for k, v in elem.items()}
        coll.insert(d)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
        if i % 1000 == 0:
            s_option = (strftime('%H:%M:%S', gmtime()), d['Id'])
            s = '{:s} : Id - {:d}\n'.format(*s_option)
            print(s, end='')
            f.write(s)

coll.ensure_index(convert('Id'))

f.close()
