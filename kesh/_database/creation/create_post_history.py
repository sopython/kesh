from pymongo import MongoClient
from lxml import etree
from dateutil.parser import parse

import pickle
from time import gmtime, strftime
import os
import re

data_dir = '../../../bin/so_data_/'
file_name = 'PostHistory.xml'
db_name = 'kesh'
coll_name = 'post_history'

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Id', 'PostHistoryTypeId', 'PostId', 'UserID'}
str_to_date = {'CreationDate'}

def convert(name):
   s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
   return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Load in a set of python ids.
with open('question_ids.pickle', 'rb') as q, \
     open('answer_ids.pickle', 'rb') as a:
    question_ids = pickle.load(q)
    answer_ids = pickle.load(a)
    ids = question_ids | answer_ids

f = open(os.path.join(data_dir, './logs/{:s}.log'.format(coll_name)), 'w')
s = 'Importing {:s} data.\n\n'.format(coll_name)
f.write(s)
print(s, end='')

i = 0
for event, elem in context:
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = dict(elem.items())
        if int(d['PostId']) in ids:
            d = {convert(k):int(v) if k in str_to_int else
                 parse(v) if k in str_to_date else
                 v for k, v in d.items()}
            coll.insert(d)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            i += 1
            if i % 10000 == 0:
                s_option = (strftime('%H:%M:%S', gmtime()), d['Id'], i)
                s = '{:s} : Id - {:d} : # - {:d}\n'.format(*s_option)
                print(s, end='')
                f.write(s)

print('Creating indices.')

coll.ensure_index(convert('Id'))

f.close()
