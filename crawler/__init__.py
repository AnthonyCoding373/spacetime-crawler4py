from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker
from crawler.central_brain import StoredData
import os
import json

class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier, worker_factory=Worker):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory
        self.central_brain = StoredData()

    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier, self.central_brain)
            for worker_id in range(self.config.threads_count)]
        for worker in self.workers:
            worker.start()

    def start(self):
        #test_counter = 0
        while not self.frontier.is_empty():
            #test_counter += 1
            #print("Time till end:", test_counter)
            #if test_counter >= 5:
            #    self.frontier.to_be_downloaded.clear() 
            print("Threads dead, restarting")
            self.start_async()
            self.join()
            

    def store_in_file(self):
        with open("general-log.txt", 'w') as file:
            file.write(f"Number of unique URLS: {len(self.central_brain.num_of_uniqueURL)} \n")
            file.write(f"Longest Page: {self.central_brain.longestpage} \n")
            file.write(f"Longest Page contains: {self.central_brain.longest_page_word_count} words\n")

            file.write("50 Most common Words:\n")
            for word in list(self.central_brain.most_frequent_words.keys())[:50]:
                file.write(f"  {word}\n")

            file.write("Unique Subdomains: \n")
            for item in self.central_brain.subdomain.keys():
                file.write(f"  {item}: {self.central_brain.subdomain[item]}\n")

    def join(self):
        for worker in self.workers:
            worker.join()
        self.central_brain.print_brain_data()
        self.store_in_file()


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
        
