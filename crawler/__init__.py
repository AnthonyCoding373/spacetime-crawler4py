from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker
import os

class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier, worker_factory=Worker):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory

    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier)
            for worker_id in range(self.config.threads_count)]
        for worker in self.workers:
            worker.start()

    def start(self):
        self.start_async()
        self.join()

    def join(self):
        for worker in self.workers:
            worker.join()

    def reset_frontier(self):
        """Resets frontier by deleteing the save file and re-initlizaitng the Frontier"""
        self.logger.info("Resetting the frontier")
        #Delete the save file
        if os.path.exists(self.config.save_file):
            os.remove(self.config.save_file)
            self.logger.info(F"Deleted save file: {self.config.save_file}")

        #Restart the frontier
        self.frontier = Frontier(self.config, restart = True)
        self.logger.info("Frontier re-initialized with seed URLs")
        
            
