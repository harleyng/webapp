from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from collections import OrderedDict
import json 

# class Image:
#     def __init__(self, title, src):
#       self.title= title
#       self.src = src
#     def __repr__(self):
#       return "C(" + repr(self.attribute) + ")"
imageList = {'img': []}

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

  def check_exist(self, value):
    value = str(value)
    for i in range(len(imageList['img'])):
      if (value in imageList['img'][i]['title']):
        return True

  # def custom_sort(self , item):
  #   print('hi', int(''.join(i for i in item['title'] if i.isdigit())))
  #   return int(''.join(i for i in item['title'] if i.isdigit()))
    

  def parse_image(self,response):
    self.count = self.count + 1
    print("-------------------", self.count)
    if (len(imageList.keys()) < 67):
      url = response.url.split('//')[-1]
      titles = response.xpath('//a[@class="td-image-wrap"]/img/@title').extract()
      srcs = response.xpath('//a[@class="td-image-wrap"]/img/@data-img-url').extract()
      # scraped_count = imageList.count()
      # print('url: {}'.format(url))
      # print('Page Title: {}'.format(titles))
      # print('Page image: {}'.format(srcs))
      for src in srcs:
        for title in titles:
          # print('Page Title: {}'.format(title))
          # print('Page image: {}'.format(src))
          if ((not(self.check_exist(value=title))) and (title.startswith('COVID-19: case'))):
            imageList['img'].append({
              'title': title,
              'src': src
            }) 
            # print('List: {}'.format(imageList.items()))
            # lambda item: int("".join([char for char in item.title if char.isdigit()]))
            # imageListOrdered = OrderedDict(sorted(imageList['img'], key=self.custom_sort))
            # print('list:' ,imageListOrdered)
            with open('data.json', 'w') as outfile:
              json.dump(imageList, outfile, indent=2)
    else:
      print('exit')
      raise CloseSpider(reason='API usage exceeded')