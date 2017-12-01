#-*- coding: utf-8 -*-
import scrapy
# import 要改为items.py中定义的类名
from SpiderDemo.items import demoItem
from scrapy.http import Request
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spriderDemo(scrapy.spiders.Spider):
    # -name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
    # 命令行中 scrapy crawl + name
    name = "spider"
    allowed_domains = ["http://10.3.210.84:4237/home/"]
    start_urls = []
    start_urls.append('http://10.3.210.84:4237/UserCenter/usercenter?querytype=1&querypolicyid=20131113132814&type=get&query=0025&query=&gx=OR&st=4efb610f4e0081f4&st=4efb610f4e0081f4&region=20131113132006&region=20131113132006&treeid=20131021155159&updatetime=0&datapid=&imtime=0&dataj=&tpf=Y&nodeid=20040921165456&username=guest&password=null&viewjbid=55555555555555&order=&orderdsc=&iswhole=0&resnum=20&maxnum=50000&pagenum=0&presnum=0')
    # 这里是分页的每个url
    for i in  range(1,5):
        start_urls.append('http://10.3.210.84:4237/UserCenter/usercenter?querytype=1&querypolicyid=20131113132814&type=get&query=0025&query=&gx=OR&st=4efb610f4e0081f4&st=4efb610f4e0081f4&region=20131113132006&region=20131113132006&treeid=20131021155159&updatetime=0&datapid=&imtime=0&dataj=&tpf=Y&nodeid=20040921165456&username=guest&password=null&viewjbid=55555555555555&order=&orderdsc=&iswhole=0&resnum=20&maxnum=50000&pagenum='+
                          str(i) + '&presnum='+ str(20*i) +'&qy0=0025&qy1=')
    custom_settings = {
		'ITEM_PIPELINES' : {
            # settings.py中BOT_NAME的名字..pipelines.JsonWithEncodingPipeline
			'SpiderDemo.pipelines.JsonWithEncodingPipeline':100,	# 开通CrawlerStorePipeline
			},
	}
    def parse(self, response):
        items = []
        for site in response.xpath('//MCCONTENT' ):
            item = demoItem()
            # count += 1
            # if count == 21:
            #     break
            # item['name'] = site.xpath('LCONTENT/text()').extract()[0]
            url = site.xpath('CONTENTLINK/text()')
            if url.extract():
                item['url'] = url.extract()[0]
                items.append(item)
        for item in items:
            # 如果不是嵌套 直接 yield  item
            # scrapy 在不同的抓取级别的Request之间传递参数的办法，
            # 下面的范例中，parse()通过meat传递给了parse_more()参数item，
            # 这样就可以再parse_more()抓取完成所有的数据后一次返回
            yield Request(item['url'],meta={'item':item}, callback=self.parse_more,dont_filter=True)


    def parse_more(self,response):
        item = response.meta['item']
        name = response.xpath('//CONTENT[1]/text()')
        author = response.xpath('//LCONTENT/text()')
        item['name'] = name.extract()[0]
        # 判断HTML标签内容为空，跳过空的
        if author.extract():
            item['author'] =  author.extract()[0]
        # item["url_id"] = response.xpath('//div[@class="main"]/div[@class="info"]/table[@class="table-1"]/tr[2]/td/text()').extract()[0]
        # site = response.xpath('//div[@class="detail"]/div[@class="info"]/table[@class="table-1"]')
        # item["url_name"] = site.xpath('tr[1]/td/text()').extract()[0]
        # item['url_enterprise'] = site.xpath('tr[2]/td/a[1]/text()').extract()[0]
        # item['url_function'] = site.xpath('tr[3]/td/text()').extract()[0]
        # item['url_usage'] = site.xpath('tr[4]/td/text()').extract()[0]

        yield item