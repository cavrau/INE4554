import scrapy
import re


class LUPASpider(scrapy.Spider):
    name = 'lupaspider'
    start_urls = ['https://g1.globo.com/fato-ou-fake/']
    allowed_domains = ['g1.globo.com']

    def parse_news(self, response):
        for next_page in response.css('a'):
            link = next_page.css('::attr(href)').get()
            if link is not None and 'fato-ou-fake' in link:
                yield response.follow(next_page, self.parse_news)
        res = {
            'title': '',
            'date': None,
            'true': True
        }
        for title in response.css('.content-head__title'):
            res['title'] = title.css('::text').get()
            res['true'] = 'FAKE' not in res['title']
            break

        res['date'] = response.css('time')[0].css('::attr(datetime)').get()
        if res['title'] != '':
            yield res


    def parse(self, response):

        for next_page in response.css('a'):
            link = next_page.css('::attr(href)').get()
            if link is not None and 'fato-ou-fake' in link:
                yield response.follow(next_page, self.parse_news)
