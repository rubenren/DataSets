# xpath_spider
import scrapy

class XpathSpider(scrapy.Spider):
    name = "xpath_spider"
    counter = 0
    page_limit = 100

    start_urls = ['http://www.investing.com/etfs/spdr-s-p-500-news']

    def parse(self, response):
        for article in response.xpath('//div[@class="textDiv"]'):
            if article.xpath("span/span[1]/text()"):
                yield {
                    'title': article.xpath('a/@title').get(),
                    'publisher': article.xpath('span/span[1]/text()').get(),
                    'date': article.xpath('span/span[2]/text()').get(),
                }
        next_page = response.xpath("//div[@id='paginationWrap']/div[3]/a/@href").get()
        if next_page is not None and self.counter < self.page_limit:
            self.counter += 1
            yield response.follow(next_page, callback=self.parse)
