from pymongo import MongoClient

class Connection(object):
    """Connection object for connecting to the mongodb database and retrieving data."""

    def __init__(self, **kwargs):
        self._options = kwargs

        self._client = None

    def connect(self):
        """Connect to the mongodb db with pymongo.MongoClient.
        :return: None
        """

        self._client = MongoClient(**self._options)

    def disconnect(self):
        """Disconnect from MongoClient.
        :return: None
        """

        if self._client is None:
            raise Exception('Cannot disconnect as no connection has successfully been made yet.')
        else:
            self._client.close()

    def __enter__(self):
        """For use with the "with" statement. Will create an open db connection.

        :return:
        """

        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """For use with the "with" statement. Will disconnect from db connection.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """

        self.disconnect()


if __name__ == '__main__':

    connection = Connection()