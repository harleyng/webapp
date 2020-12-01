from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from collections import OrderedDict
import json 
import re 

# class Image:
#     def __init__(self, title, src):
#       self.title= title
#       self.src = src
#     def __repr__(self):
#       return "C(" + repr(self.attribute) + ")"
imageList = {}

class CTScanImageSpider(CrawlSpider):
  name = 'ct'
  allowed_domains = ['radiopaedia.org']
  start_urls = ['https://radiopaedia.org/articles/covid-19-4?lang=us']
  # extract link in covid-19-database end with a number of page
  # dataset missing case 8
  rules = [Rule(LinkExtractor( allow=(r'^https://radiopaedia.org/cases/covid-19-pneumonia'), 
                                deny=(r'/revisions')
                              ),  
                callback='parse_image',
                follow=True)]
  # COUNT_MAX = 5
  case = 0
  def parse_image(self,response):
    self.case = self.case + 1
    case_count = "Case " + str(self.case)

    print("-------------------", self.case)
    if (len(imageList.keys()) < 1000):
      url = response.url.split('//')[-1]
      presentation = response.xpath('//div[@id="case-patient-presentation"]/p/text()').get()
      titles = response.xpath('//div[@class="study-desc"]/h2/text()').extract()
      srcs = response.xpath('//img[@id="offline-workflow-study-large-image"]/@src').extract()
      # scraped_count = imageList.count()
      print('url: {}'.format(url))
      print('Page Title: {}'.format(titles))
      print('Page image: {}'.format(srcs))
      # print('Presentation: {}'.format(presentation))
      # Age and Gender
      age = response.xpath('//div[@id="case-patient-data"]/div[1]/text()').extract()
      gender = response.xpath('//div[@id="case-patient-data"]/div[2]/text()').extract()
      for a in age:
        age_pattern = re.compile('^ [0-99]')
        if age_pattern.match(a):   
          a.replace('\n', '')       
          age = a
      for g in gender:
        gender_pattern = re.compile('^ Female| Male')
        if gender_pattern.match(g):
          g.replace('\n', '')    
          gender = g

      # for src in srcs:
      #   for title in titles:
      #     print('Page Title: {}'.format(title))
      #     print('Page image: {}'.format(src))
      # for u in url:
      
      imageList[case_count] = {
        'presentation': presentation,
        'age': age,
        'gender': gender,
        # 'img': {
        #   'title': title,
        #   'src': src
        # }
      }
      with open('data.json', 'w') as outfile:
        json.dump(imageList, outfile, indent=2)
    else:
      print('exit')
      raise CloseSpider(reason='API usage exceeded')