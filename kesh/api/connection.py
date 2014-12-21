from pymongo import MongoClient


class Connection(object):

    def __init__(self):
        super().__init__()


class MongoConnection(Connection):
    """Connection object for connecting to the mongodb database and retrieving data."""

    def __init__(self, db, mongo_options={}):
        super().__init__()

        self.client = MongoClient(**mongo_options)
        self.db = self.client[db]


    def query(self, d):

        coll_name = d.pop('collection', None)
        if coll_name is None:
            raise Exception('Collection param not found in query.')

        coll = self.db[coll_name]

        if 'id' in d:
            return coll.find_one(d)

        if 'ids' in d.keys():
            return list(coll.find({'id':{'$in':d['ids']}}))

        if 'all' in d and d['all']:
            return coll.find()


    def __enter__(self):
        """For use with the "with" statement. Will create an open db connection.

        :return: Client connection.
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """For use with the "with" statement. Will disconnect from db connection.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """

        self.client.close()


if __name__ == '__main__':

    with MongoConnection() as conn:
        print(conn)