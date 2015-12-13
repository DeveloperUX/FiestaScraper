import scrapy
import re

from scrapy import Spider
from scrap.items import ScrapItem


class Scrapider(Spider):
    name = "Scrapider"
    allowed_domains = ["http://foodtruckfiesta.com"]
    start_urls = [
        "http://foodtruckfiesta.com",
    ]

    def parse(self, response):

        for truckUrl in response.xpath('//*[@id="blogroll"][1]/li[1]/ul/li/a'):

            link = truckUrl.xpath('.//@href').extract()[0]
            linkText = truckUrl.xpath('.//text()').extract()[0] #.re('^[^\(]+')

            name = linkText.split(' (')[0]
            handle = linkText.split(' (')[1].split(')')[0]

            # Save the info to our Item
            item = ScrapItem()
            item['name'] = name
            item['handle'] = handle
            item['url'] = response.urljoin(link)

            request = scrapy.Request(url=item['url'], dont_filter=True, callback=self.parse_image)
            request.meta['item'] = item

            yield request

    def parse_image(self, response):
        item = response.meta['item'];

        item['image'] = response.xpath('//*[@id="content"]//a/img/@src')[0].extract()
        print item['image']

        return item
