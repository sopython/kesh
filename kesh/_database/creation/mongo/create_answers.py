import pickle
from time import gmtime, strftime
import os

from pymongo import MongoClient
from lxml import etree
from kesh._database.creation.mongo.tools import schemas


def create_answers():

    data_dir = '../../../bin/so_data_/'
    file_name = 'Posts.xml'
    db_name = 'kesh'
    coll_name = 'answers'

    # Load in a set of python question ids.
    with open('question_ids.pickle', 'rb') as f:
        question_ids = pickle.load(f)

    client = MongoClient()
    db = client[db_name]
    coll = db[coll_name]

    context = etree.iterparse(os.path.join(data_dir, file_name),
                              events=('start', 'end'))

    f = open(os.path.join(data_dir, './logs/{:s}.log'.format(coll_name)), 'w')
    s = 'Importing {:s} data.\n\n'.format(coll_name)
    f.write(s)
    print(s, end='')

    i = 0
    answer_ids = set()

    schema = schemas[coll_name]

    for event, elem in context:
        if event == 'end' and elem.tag == 'row':
            # Create a dictionary and convert any necessary fields.
            d, e = schema.load(dict(elem.items()))
            if d['post_type_id'] == 2 and d['parent_id'] in question_ids:
                coll.insert(d)
                answer_ids.add(d['id'])
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
                i += 1
                if i % 1000 == 0:
                    s_option = (strftime('%H:%M:%S', gmtime()), d['id'])
                    s = '{:s} : Id - {:d}\n'.format(*s_option)
                    print(s, end='')
                    f.write(s)

    coll.ensure_index('id')

    f.close()

    with open('answer_ids.pickle', 'wb') as f:
        pickle.dump(answer_ids, f)

