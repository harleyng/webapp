from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json 
imageList = []
class CTScanImageSpider(CrawlSpider):
  name = 'endless'

  allowed_domains = ['radiopaedia.org']

  start_urls = ['https://radiopaedia.org/cases/covid-19-pneumonia-4']

  rules = [Rule(LinkExtractor(allow=r'.*'), 
                callback='parse_image',
                follow=True)]

  def parse_image(self,response):
    url = response.url
    src = response.css('img::attr(src)').extract()
    print('Page URL: {}'.format(url))
    print('Page image: {}'.format(src))
    imageList.append({
      'pageURL': url,
      'imageSrc': src
    })
    with open('data.txt', 'a') as outfile:
      json.dump(imageList, outfile)