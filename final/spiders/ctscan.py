import scrapy

class CTScanImageSpider(scrapy.Spider):
  name = 'CTScanImage'

  def start_requests(self):
    urls = ['https://vietnamtimes.org.vn/coronavirus-what-happens-to-peoples-lungs-if-they-get-covid-19-18693.html']

    return [scrapy.Request(url=url, callback=self.parse) for url in urls]

  def parse(self, response):
    url = response.url
    page = url.split('/')[-1]
    filename = 'image-%s' %page
    print('URL is: {}'.format(url))
    with open(filename, 'wb') as file:
      file.write(response.body)
    print('Saved file %s' % filename)