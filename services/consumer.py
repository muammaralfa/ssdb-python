import asyncio
import json
import time
from config.base import app_setting
from services.producer import Producer
from connection.beanstalk_conn import Connection as BeanstalkConnection
from greenstalk import TimedOutError
from loguru import logger


class Consumer:
    def __init__(self):
        self.tube: str = app_setting.BEANSTALK_TUBE_DATA
        self.beanstalk_conn = BeanstalkConnection().connect()
        self.producer = Producer()

    def consume(self):
        """
        biasanya ssdb digunakan bersamaan dengan beanstalk.
        beanstalk berperan untuk menyimpan antrian id data di ssdb
        dan ssdb berperan untuk penyimpanan antrian datanya,
        lalu kita mengambil data di ssdb menggunakan id yang didapatkan dari beanstalk

        """
        self.beanstalk_conn.watch(tube=self.tube)
        logger.info("start consuming...")
        try:
            while True:
                job = self.beanstalk_conn.reserve(timeout=60)
                if job:
                    message = json.loads(job.body)
                    _id = message['_id']
                    logger.info(message)
                    self.producer.produce_id_into_beanstalk(self.tube, _id)
                    self.producer.produce_into_ssdb(self.tube, data=message)
                    self.beanstalk_conn.delete(job)

        except TimedOutError:
            logger.warning("No job available")
            time.sleep(30)


