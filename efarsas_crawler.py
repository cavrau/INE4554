import scrapy



class EFarsasSpider(scrapy.Spider):
    name = 'efarsasspider'
    start_urls = ['https://www.e-farsas.com/']
    allowed_domains = ['e-farsas.com']

    def parse_news(self, response):
        for next_page in response.css('a'):
            yield response.follow(next_page, self.parse_news)
        res = {
            'title': [],
            'date': None,
            'true': True
        }
        _class = []
        for header in response.css('.td-main-content-wrap h1'):
            res['title'].append(header.css('::text').get())
        for strong in response.css('.td-main-content-wrap .vc_column_container  p strong'):
            _class.append(strong.css('::text').get())
        _pass = True
        for f in response.css('.tdb-entry-category'):
            if 'Falso' in f.css('::text').get():
                res['true'] = False
            elif f.css('::text').get() in ['E-farsas TV', 'Podcasts']:
                _pass = False
        if _pass and len(_class) != 0:
            res['date'] = response.css('time')[0].css('::attr(datetime)').get()
            yield res
    
    def parse(self, response):

        for next_page in response.css('a'):
            yield response.follow(next_page, self.parse_news)
