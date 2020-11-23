from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from collections import OrderedDict
import json 

imageList = {}
class CTScanImageSpider(CrawlSpider):
  name = 'endless'
  allowed_domains = ['sirm.org']
  start_urls = ['https://www.sirm.org/en/category/articles/covid-19-database/']
  # extract link in covid-19-database end with a number of page
  # dataset missing case 8
  rules = [Rule(LinkExtractor(allow=r'(^https://www.sirm.org/en/category/articles/covid-19-database)($[1-9]|/)'), 
                callback='parse_image',
                follow=True)]
  # COUNT_MAX = 5
  count = 0
  def parse_image(self,response):
    self.count = self.count + 1
    print("-------------------", self.count)
    if (len(imageList.keys()) < 67):
      url = response.url.split('//')[-1]
      titles = response.xpath('//a[@class="td-image-wrap"]/img/@title').extract()
      srcs = response.xpath('//a[@class="td-image-wrap"]/img/@data-img-url').extract()
      # limit = 10
      # scraped_count = imageList.count()
      print('url: {}'.format(url))
      print('Page Title: {}'.format(titles))
      print('Page image: {}'.format(srcs))
      for src in srcs:
        for title in titles:
          if ((title not in imageList) and (title.startswith('COVID-19: case'))):
            imageList[title] = src
            # print('List: {}'.format(imageList.items()))
            imageListOrdered = OrderedDict(sorted(imageList.items(), key=lambda x: int("".join([i for i in x[0] if i.isdigit()]))))
            print('list:' ,imageListOrdered)
            with open('data.json', 'w') as outfile:
              json.dump(imageListOrdered, outfile, indent=2)
    else:
      print('exit')
      raise CloseSpider(reason='API usage exceeded')
