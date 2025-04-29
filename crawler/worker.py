from threading import Thread
from bs4 import BeautifulSoup
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.num_of_uniqueURL = set()
        self.longestpage = "Does not Exist"
        self.longest_page_word_count = 0
        self.subdomain = {}  
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        #Testing if Part 1,2,4 work
        globaltimer = 0
        while True:
            tbd_url = self.frontier.get_tbd_url()
            globaltimer = globaltimer + 1
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
                
            resp = download(tbd_url, self.config, self.logger)
            if resp is None or not scraper.is_valid(tbd_url) or resp.status == '404' or resp.raw_response is None:
                self.logger.warning(f"Empty response: {tbd_url}")
                self.frontier.mark_url_complete(tbd_url)
                continue
            current_url = tbd_url.split('#')[0]
            self.num_of_uniqueURL.add(current_url)
            parsed_info = BeautifulSoup(resp.raw_response.content, "html.parser")
            gathered_text = parsed_info.get_text()
            all_valued_text = gathered_text.split()
            number_of_words = len(all_valued_text)
            if (number_of_words < 50):
                self.frontier.mark_url_complete(tbd_url)
                self.logger.warning(f"Too Small Data Set: {tbd_url}")
                continue
            current_authority = current_url.split('//')[-1]
            current_subdomain = current_authority.split('/')[0]
            if number_of_words > self.longest_page_word_count:
                self.longest_page_word_count = number_of_words
                self.longestpage = tbd_url
            if current_subdomain.endswith("uci.edu"):
                if current_subdomain not in self.subdomain:
                    self.subdomain[current_subdomain] = 1
                else:
                    self.subdomain[current_subdomain] = self.subdomain[current_subdomain] + 1
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
            #Testing if Part 1,2,4 work
            if globaltimer == 10:
                print("CHECKING DATA:                      ")
                print("Number of uniqueURLS: ", len(self.num_of_uniqueURL))
                print("Longest page: " + self.longestpage)
                print("Longest page contains ", self.longest_page_word_count, " words")
                print("All Detected Subdomains: ")
                for item in self.subdomain:
                    print(item, self.subdomain[item])


        print("Number of uniqueURLS: ", len(self.num_of_uniqueURL))
        print("Longest page: " + self.longestpage)
        print("Longest page contains ", self.longest_page_word_count, " words")
        print("All Detected Subdomains: ")
        for item in self.subdomain:
            print(item, self.subdomain[item])
