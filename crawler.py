import os
import re
import scrapy
import logging
import urllib.request
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class FourChanSpider(scrapy.Spider):
    name = "4chan Spider"
    allowed_domains = ["boards.4channel.org", "boards.4chan.org"]
    start_urls = [
            "https://boards.4channel.org/g/catalog",
            "https://boards.4chan.org/h/catalog",
            "https://boards.4chan.org/e/catalog",
            "https://boards.4chan.org/d/catalog",
            "https://boards.4chan.org/aco/catalog"
            ]
    link_extractor = LinkExtractor()

    data_dir = "data"
    archive_dir = os.path.join(data_dir, "archive")
    best_dir = os.path.join(data_dir, "best")
    trash_dir = os.path.join(data_dir, "trash")

    chan_url = None
    chan_url_long = "boards.4channel.org"
    chan_url_short = "boards.4chan.org"
    urls = []

    def parse(self, response):
        # skip previously crawled urls
        if response.url in self.urls:
            return
        else:
            # print(f"URL: {response.url}")
            self.urls.append(response.url)

        # get board
        self.chan_url = self.chan_url_long if "boards.4channel.org" in response.url else self.chan_url_short if "boards.4chan.org" in response.url else None
        if self.chan_url is None:
            return
        start = response.url.find(self.chan_url) + len(self.chan_url) + 1
        board = response.url[start:response.url.find("/", start)]

        # crawl for /general/ threads
        if "/catalog" in response.url:
            js = response.xpath("//script[@type='text/javascript']").extract()[2]
            threads = re.findall(r'"\d{7,9}":{.+?(?=(?:,"\d{7,9}")|(?:}}))', js)

            for thread in threads:
                thread_id = thread[1:thread.find('":{')]
                sub = thread[thread.find('"sub":"')+len('"sub":"'):thread.find('","teaser"')]

                if "sdg" in sub or "hdg" in sub or "ddg" in sub or "asdg" in sub:
                    print(f"THREAD: /{board}/thread/{thread_id} FROM CATALOG: {sub}")
                    yield scrapy.Request(f"https://{self.chan_url}/{board}/thread/{thread_id}")

        # crawl inside /general/ threads
        if "/thread/" in response.url:
            # create dirs if they don't exist
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(archive_dir, exist_ok=True)
            os.makedirs(best_dir, exist_ok=True)
            os.makedirs(trash_dir, exist_ok=True)
            title = response.xpath("/html/head/meta[3]").extract_first()
            if "sdg" in title or "hdg" in title or "ddg" in title or "asdg" in title:
                # crawl old /general/ threads
                for link in set([link.url.split("#")[0] for link in self.link_extractor.extract_links(response) if link.url.startswith(f"https://boards.4channel.org/{board}/thread/") and link.url[-1].isnumeric()]):
                    yield scrapy.Request(link)

                # check for catbox.moe links
                for link in re.findall("files\.catbox\.moe/.{1,20}\.\w{3}", response.text):
                    if link.lower()[-3:] in ["jpg", "png"]:
                        link = link.replace("<wbr>", "")
                        new_path = os.path.join(self.data_dir, link.split("/")[-1])
                        archive_path = os.path.join(self.archive_dir, link.split("/")[-1])
                        best_path = os.path.join(self.best_dir, link.split("/")[-1])
                        trash_path = os.path.join(self.trash_dir, link.split("/")[-1])
                        if not os.path.exists(new_path) and not os.path.exists(archive_path) and not os.path.exists(best_path) and not os.path.exists(trash_path):
                            print(f"DOWNLOAD: {link}")
                            # urllib.request.urlretrieve("https://" + link, new_path)
                            r = requests.get("https://" + link)
                            with open(new_path, 'wb') as outfile:
                                outfile.write(r.content)
                        else:
                            print(f"SKIP: {link}")

                # check for litterbox links
                for link in re.findall("litter\.catbox\.moe/.{1,20}\.\w{3}", response.text):
                    if link.lower()[-3:] in ["jpg", "png"]:
                        link = link.replace("<wbr>", "")
                        new_path = os.path.join(self.data_dir, link.split("/")[-1])
                        archive_path = os.path.join(self.archive_dir, link.split("/")[-1])
                        best_path = os.path.join(self.best_dir, link.split("/")[-1])
                        trash_path = os.path.join(self.trash_dir, link.split("/")[-1])
                        if not os.path.exists(new_path) and not os.path.exists(archive_path) and not os.path.exists(best_path) and not os.path.exists(trash_path):
                            print(f"DOWNLOAD: {link}")
                            # urllib.request.urlretrieve("https://" + link, new_path)
                            r = requests.get("https://" + link)
                            with open(new_path, 'wb') as outfile:
                                outfile.write(r.content)
                        else:
                            print(f"SKIP: {link}")

                # check for catgirlsare.sexy links
                for link in re.findall("b\.catgirlsare\.sexy/.{1,20}\.\w{3}", response.text):
                    if link.lower()[-3:] in ["jpg", "png"]:
                        link = link.replace("<wbr>", "")
                        new_path = os.path.join(self.data_dir, link.split("/")[-1])
                        archive_path = os.path.join(self.archive_dir, link.split("/")[-1])
                        best_path = os.path.join(self.best_dir, link.split("/")[-1])
                        trash_path = os.path.join(self.trash_dir, link.split("/")[-1])
                        if not os.path.exists(new_path) and not os.path.exists(archive_path) and not os.path.exists(best_path) and not os.path.exists(trash_path):
                            print(f"DOWNLOAD: {link}")
                            # urllib.request.urlretrieve("https://" + link, new_path)
                            r = requests.get("https://" + link)
                            with open(new_path, 'wb') as outfile:
                                outfile.write(r.content)
                        else:
                            print(f"SKIP: {link}")


if __name__ == "__main__":
    logging.getLogger('scrapy').propagate = False

    c = CrawlerProcess({
        "USER_AGENT": "Naa",
        "ROBOTSTXT_OBEY": False,
        "HTTPCACHE_ENABLED": False,
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"
    })
    c.crawl(FourChanSpider)
    c.start()
