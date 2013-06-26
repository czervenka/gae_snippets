
import logging
from threading import Thread
from time import sleep
from datetime import datetime

class ThreadPool(object):

    def __init__(self, pool_size=30, tick=0.3):
        self._pool_size = pool_size
        self._jobs = []
        self._pool = []
        self._tick = tick

    def add(self, callback, *args, **kwargs):
        self._jobs.append((callback, args, kwargs))

    def jobs_count(self):
        return len(self._pool) + len(self._jobs)

    def finish(self):
        self._end_time = datetime.now()
        logging.debug('Finished in %s.' % (self._start_time - self._end_time))

    def start(self):
        self._start_time = datetime.now()
        logging.debug('Starting.')

    def tick(self):
        pool_size = len(self._pool)
        jobs_count = len(self._jobs)
        logging.debug('%s running %d / %d.' % (self.__class__.__name__, pool_size, pool_size + jobs_count))
        sleep(self._tick)

    def run(self):
        self.start()
        self._feed_pool()
        while True:
            self._clean_pool()
            if not self._feed_pool():
                break
            self.tick()
        self.finish()

    def _clean_pool(self):
        self._pool = filter(lambda t: t.is_alive(), self._pool)
        if not self._pool:
            self.finish()

    def _feed_pool(self):
        pool_size = len(self._pool)
        while pool_size < self._pool_size:
            try:
                job = self._jobs.pop(0)
            except IndexError:
                return 0
            thread = Thread(target=job[0], args=job[1], kwargs=job[2])
            self._pool.append(thread)
            logging.debug('Adding job')
            thread.start()
            pool_size += 1
        return len(self._jobs)
