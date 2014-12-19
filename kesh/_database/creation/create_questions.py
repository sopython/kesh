from pymongo import MongoClient
from lxml import etree
from dateutil.parser import parse

import pickle
from time import gmtime, strftime
import os
import re

data_dir = '../../../bin/so_data_/'
file_name = 'Posts.xml'
db_name = 'kesh'
coll_name = 'questions'

client = MongoClient()
db = client[db_name]
coll = db[coll_name]

context = etree.iterparse(os.path.join(data_dir, file_name), 
                          events=('start', 'end'))

str_to_int = {'Id', 'PostTypeId', 'ParentId', 'Score', 'ViewCount',
              'OwnerUserId', 'AcceptedAnswerId', 'AnswerCount', 'CommentCount',
              'FavoriteCount', 'LastEditorUserId'}
str_to_date = {'CreationDate', 'LastActivityDate', 'LastEditDate',
               'CommunityOwnedDate', 'ClosedDate'}
str_to_list = {'Tags'}

python_tags = {'python', 'python-2.7', 'python-3.x', 'python-2.x', 'python-3.3', 'python-2.6', 'python-3.4', 'python-2.5',
               'python-3.2', 'python-2.4', }

def convert(name):
   s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
   return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_tags(s):
    return [i.strip('<') for i in s.split('>')[:-1]]

f = open(os.path.join(data_dir, './logs/{:s}.log'.format(coll_name)), 'w')
s = 'Importing {:s} data.\n\n'.format(coll_name)
f.write(s)
print(s, end='')

i = 0
question_ids = set()

for event, elem in context:
    if event == 'end' and elem.tag == 'row':
        # Create a dictionary and convert any necessary fields.
        d = {convert(k):int(v) if k in str_to_int else
             parse(v) if k in str_to_date else
             convert_tags(v) if k in str_to_list else
             v for k, v in elem.items()}
        if d['post_type_id'] == 1 and set(d['tags']).intersection(python_tags):
            coll.insert(d)
            # Add the post id to a set for pickling. This will be used
            # in other creation files to only create answers/comments/etc
            # that belong to Python questions.
            question_ids.add(d['id'])
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            i += 1
            if i % 1000 == 0:
                s_option = (strftime('%H:%M:%S', gmtime()), d['id'])
                s = '{:s} : Id - {:d}\n'.format(*s_option)
                print(s, end='')
                f.write(s)

print('Finished importing, now creating indices.')

coll.ensure_index(convert('id'))

f.close()

with open('question_ids.pickle', 'wb') as f:
    pickle.dump(question_ids, f)
