# -*- coding: utf-8 -*-
import scrapy
import csv
import os

class Top250tvSpider(scrapy.Spider):
    name = 'top250tv'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/toptv/']

    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ['Rank','Title','Ratting'],
    }

    def parse(self, response):
        
        links=response.xpath('//*[@class="titleColumn"]/a/@href').extract()      
      

        for link in links:
            absurl=response.urljoin(link)
            yield scrapy.Request(absurl,callback=self.parse_tv)

    
    def parse_tv(self,response):

        name=response.xpath('//h1/text()').extract_first()
        ratting=response.xpath('//*[@itemprop="ratingValue"]/text()').extract_first()
        ranking=response.xpath('//*[@class="article highlighted"]/strong/a/text()').extract_first()
        ranking=ranking.split()[3][1:]

        yield { 'Rank' : ranking,
                'Title': name,
                'Ratting': ratting
                }

    def close(self, reason):

        with open('out_tv.csv') as sample, open('top250tv.csv', "w") as out:
            csv1=csv.reader(sample)
            header = next(csv1, None)
            csv_writer = csv.writer(out)
            if header:
                csv_writer.writerow(header)
            csv_writer.writerows(sorted(csv1, key=lambda x:int(x[0])))
        
        os.remove("out_tv.csv")