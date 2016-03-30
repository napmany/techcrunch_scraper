from grab import Grab
from pymongo.errors import DuplicateKeyError
from helpers import db as dbhelper
import sys
import logging


class Scraper:
    def __init__(self, limit=30):
        self.initial_url = 'http://techcrunch.com/'
        self.limit = int(limit)
        self.count = 0

    def scrape(self, url=None):
        if url is None:
            url = self.initial_url
        g = Grab()
        g.go(url)

        news_blocks = g.doc.select("//li[contains(@class, 'river-block')]")

        for news_block in news_blocks:
            self.count += 1
            if self.count >= self.limit:
                return

            try:
                news_link = news_block.select('.//h2/a')[0]
                news_title = news_link.text()
                news_href = g.make_url_absolute(news_link.attr('href'))
            except IndexError as e:
                continue

            if dbhelper.get_entries({'href': news_href}).count():
                print("News %s already exists" % news_href)
                continue

            news_grab = Grab()
            news_grab.go(news_href)

            try:
                news_text = news_grab.doc.select('.//div[contains(@class, "article-entry")]')[0].text(smart=True)
            except IndexError as e:
                news_text = ''

            print('%s: %s' % (news_title, news_href))

            try:
                id = dbhelper.save_entry({
                    "href": news_href,
                    "title": news_title,
                    "text": news_text
                })

                print(str(id))
            except DuplicateKeyError as e:
                print("News %s already exists" % news_href)

        if self.count < self.limit:
            try:
                next_page_url = g.make_url_absolute(g.doc.select('//ol[contains(@class, "pagination")]//li[contains(@class, "next")]//a')[0].attr('href'))
                self.scrape(next_page_url)
            except IndexError as e:
                print('No more news')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    scraper = Scraper(*sys.argv[1:])
    scraper.scrape()
