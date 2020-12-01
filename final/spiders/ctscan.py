from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, HtmlResponse
from collections import OrderedDict
import json 
import re
import scrapy_splash
import scrapy

script = """
function main(splash)
    assert(splash:go(splash.args.url))
    return splash:evaljs("document.title")
end
"""

# ...
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
  rules = [Rule(LinkExtractor( allow=(r'^https://radiopaedia.org/cases/covid-19-pneumonia'), 
                                deny=(r'/revisions|lang=us')
                              ),  
                callback='parse_image',
                process_request = "use_splash",
                follow=True)]
  # COUNT_MAX = 5
  case = 0

  def _requests_to_follow(self, response):
    if not isinstance(
                response,
                (HtmlResponse, scrapy_splash.response.SplashJsonResponse, scrapy_splash.response.SplashTextResponse)):
            return
    seen = set()
    for n, rule in enumerate(self._rules):
        links = [lnk for lnk in rule.link_extractor.extract_links(response)
                  if lnk not in seen]
        if links and rule.process_links:
            links = rule.process_links(links)
        for link in links:
            seen.add(link)
            r = self._build_request(n, link)
            yield rule.process_request(r)

  def use_splash(self, request):
    request.meta['splash']={
        'args': {
            'wait': 0.5,
        },
        'endpoint': 'render.html',
    }
    return request

  # def start_requests(self):
  #    for url in self.start_urls:
  #       yield scrapy.Request(url, self.parse_image, meta={
  #           'splash': {
  #               'endpoint': 'render.html',
  #               'args': {'wait': 0.5}
  #           }
  #       })

            
  # def parse(self, response):
  #     # Get the next page and yield Request
  #     # next_selector = response.xpath('//*[@title="Next"]/@href')
  #     # for url in next_selector.extract():
  #     #     yield SplashRequest(url, endpoint='execute',
  #     #                         args={'lua_source': script2})

  #     # Get URL in page and yield Request
  #     url_selector = response.xpath(
  #         '//div[@class="image-grid-image-container"]/a/@href')
  #     for url in url_selector.extract():
  #         yield SplashRequest(url, callback=self.parse_image,
  #                             endpoint='execute',
  #                             args={'lua_source': script2})

  def parse_image(self,response):
    self.case = self.case + 1
    case_count = "Case " + str(self.case)

    print("-------------------", self.case)
    if (len(imageList.keys()) < 1000):
      url = response.url.split('//')[-1]
      presentation = response.xpath('//div[@id="case-patient-presentation"]/p/text()').extract()
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
      if not srcs:
        pass
      else:
        imageList[case_count] = {
          'presentation': presentation,
          'age': age,
          'gender': gender,
          'img': []
        }
        for i in range(len(srcs)):
          # print('Page image: {}'.format(src))
          # print('Page Title: {}'.format(title))
          if i >= len(titles):
            titles.append('') 
          imageList[case_count]['img'].append({
            'title': titles[i],
            'src': srcs[i],
          })


      with open('data.json', 'w') as outfile:
        json.dump(imageList, outfile, indent=2)
    else:
      print('exit')
      raise CloseSpider(reason='API usage exceeded')