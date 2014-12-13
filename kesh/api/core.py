from pymongo import MongoClient

class Connection(object):
    """Connection object for connecting to the mongodb database and retrieving data."""

    def __init__(self, **kwargs):
        self._options = kwargs

    def _connect(self):
        """Connect to the mongodb db with pymongo.MongoClient.
        :return: None
        """

        self._client = MongoClient(**self._options)

    def _disconnect(self):
        """Disconnect from MongoClient.
        :return: None
        """

        self._client.close()

    def __enter__(self):
        """For use with the "with" statement. Will create an open db connection.

        :return:
        """

        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """For use with the "with" statement. Will disconnect from db connection.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """

        self._disconnect()


if __name__ == '__main__':

    with Connection() as connection:
        print(connection)