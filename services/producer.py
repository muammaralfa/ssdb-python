import json

from connections.beanstalk_conn import Connection as ConnectionBeanstalk
from connections.ssdb_conn import Connection as ConnectionSsdb


class Producer:
    def __init__(self):
        self.conn_beanstalk = ConnectionBeanstalk().connect()
        self.conn_ssdb = ConnectionSsdb().connect()

    def produce_id_into_beanstalk(self, tube, _id: str):
        self.conn_beanstalk.use(tube)
        self.conn_beanstalk.put(
            json.dumps({"id": _id}),
            ttr=3600,
            priority=2 ** 16,
            delay=10
        )
        print(f">>> stored _id || {_id}")

    def produce_into_ssdb(self, tube, data: dict):
        """
        store data into sscb server
        :param tube:
        :param data:
        :return:
        """
        self.conn_ssdb.hset(
            tube,
            data['id'],
            json.dumps(data)
        )
        print(f">>> data store into tube ({tube})")