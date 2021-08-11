import scrapy
import re


class LUPASpider(scrapy.Spider):
    name = 'lupaspider'
    start_urls = ['https://piaui.folha.uol.com.br/lupa/']
    allowed_domains = ['piaui.folha.uol.com.br']

    def parse_news(self, response):
        for next_page in response.css('a'):
            if 'http' in next_page.css('::attr(href)').get() and 'lupa' in next_page.css('::attr(href)').get():
                yield response.follow(next_page, self.parse_news)
        
        titles = []
        date = ''
        true = []
        for title in response.css('p b'):
            title_text = title.css('::text').get()
            if len(title_text.split(' ')) > 5:
                titles.append(title_text)

        for tag in response.css('.post-inner .etiqueta'):
            true.append(tag.css('::text').get() == "VERDADEIRO")
        
        print(titles,true)
        if len(true) > 0 and len(titles) == len(true):
            date = response.css('.bloco-meta')[0].css('::text').get()
            date = re.findall(r'\d{2}\.\w{3}\.\d{4}', date)[0]
            for i, title in enumerate(titles):
                yield {
                    'title': title,
                    'date': date,
                    'true': true[i]
                }
    
    def parse(self, response):

        for next_page in response.css('a'):
            if 'http' in next_page.css('::attr(href)').get() and 'lupa' in next_page.css('::attr(href)').get():
                yield response.follow(next_page, self.parse_news)
