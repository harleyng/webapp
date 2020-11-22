from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from publicsuffix import PublicSuffixList, fetch
import json 

imageList = []
class CTScanImageSpider(CrawlSpider):
  name = 'endless'
  allowed_domains = ['sirm.org']
  start_urls = ['https://www.sirm.org/en/category/articles/covid-19-database/']
  rules = [Rule(LinkExtractor(allow=r'.*'), 
                callback='parse_image',
                follow=True)]
  COUNT_MAX = 5
  count = 0
  def parse_image(self,response):
    self.count = self.count + 1
    print("-------------------", self.count)
    if (self.count < self.COUNT_MAX):
      url = response.url.split('//')[-1]
      src = response.xpath('//a[@class="td-image-wrap"]/img/@src').extract()
      # limit = 10
      # scraped_count = imageList.count()
      print('Page URL: {}'.format(url))
      print('Page image: {}'.format(src))
      imageList.append({
        'pageURL': url,
        'imageSrc': src
      })
      with open('data.txt', 'a') as outfile:
        json.dump(imageList, outfile, indent=2)
    else:
      return
