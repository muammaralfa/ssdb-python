import json

from ssdb import SSDB
from config.base import app_setting


class Connection:
    def __init__(self):
        pass

    def connect(self):
        """
            membuka connection ke server sscb
        :return:
        """
        ssdb = SSDB(app_setting.SSDB_HOST, int(app_setting.SSDB_PORT))
        return ssdb

    def is_exists(self, conn: SSDB, tube, _id):
        """
        menegcek apakah data exists di server ssdb
        :param conn:
        :param tube:
        :param _id:
        :return: Boolean True jika ada, false jika tidak
        """
        return conn.hget(tube, _id)

    def get_data(self, key):
        """
        mengambil data di server ssdb
        :param key:
        :return:
        """
        value = self.connect().get(key)
        if not value:
            return json.load(value)


