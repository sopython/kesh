from time import gmtime, strftime
import os

from pymongo import MongoClient
from lxml import etree
from kesh._database.creation.mongo.tools import schemas


def create_users():

    data_dir = '../../../bin/so_data_/'
    file_name = 'Users.xml'
    db_name = 'kesh'
    coll_name = 'users'

    client = MongoClient()
    db = client[db_name]
    coll = db[coll_name]

    context = etree.iterparse(os.path.join(data_dir, file_name),
                              events=('start', 'end'))

    f = open(os.path.join(data_dir, './logs/{:s}.log'.format(coll_name)), 'w')
    f.write('Importing {:s} data.\n\n'.format(coll_name))

    schema = schemas[coll_name]

    for i, (event, elem) in enumerate(context):
        if event == 'end' and elem.tag == 'row':
            # Create a dictionary and convert any necessary fields.
            d, e = schema.load(dict(elem.items()))
            coll.insert(d)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
            if i % 50000 == 0:
                s_option = (strftime('%H:%M:%S', gmtime()), d['id'])
                s = '{:s} : Id - {:d}\n'.format(*s_option)
                print(s, end='')
                f.write(s)

    coll.ensure_index('id')

    f.close()

