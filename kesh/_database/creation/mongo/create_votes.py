import pickle
from time import gmtime, strftime
import os

from pymongo import MongoClient
from lxml import etree
from kesh._database.creation.mongo.tools import schemas


def create_votes():

    data_dir = '../../../bin/so_data_/'
    file_name = 'Votes.xml'
    db_name = 'kesh'
    coll_name = 'votes'

    client = MongoClient()
    db = client[db_name]
    coll = db[coll_name]

    context = etree.iterparse(os.path.join(data_dir, file_name),
                              events=('start', 'end'))

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

    schema = schemas[coll_name]

    i = 0
    for event, elem in context:
        if event == 'end' and elem.tag == 'row':
            # Create a dictionary and convert any necessary fields.
            d, e = schema.load(dict(elem.items()))
            if d['post_id'] in ids:
                coll.insert(d)
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
                i += 1
                if i % 50000 == 0:
                    s_option = (strftime('%H:%M:%S', gmtime()), d['id'], i)
                    s = '{:s} : Id - {:d} : # - {:d}\n'.format(*s_option)
                    print(s, end='')
                    f.write(s)

    print('Creating indices.')

    coll.ensure_index('id')

    f.close()
