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
    allowed_domains = ["https://lostcherry.github.io/"]
    start_urls = []
    start_urls.append('https://lostcherry.github.io/')   # 这里是分页的每个url
    for i in range(2, 4):
        start_urls.append('https://lostcherry.github.io/page/'+
                          str(i) + '/')
    custom_settings = {
		'ITEM_PIPELINES' : {
            # settings.py中BOT_NAME的名字..pipelines.JsonWithEncodingPipeline
			'SpiderDemo.pipelines.JsonWithEncodingPipeline':100,	# 开通CrawlerStorePipeline
			},
	}
    def parse(self, response):
        items = []
        for site in response.xpath('//section[@id="posts"]'):   # //取id值为post的所有section节点
            # @取href属性的值
            urls = site.xpath('//a[@class="post-title-link"]//@href')
            articles = site.xpath('//header[@class="post-header"]')
            domain_url = "https://lostcherry.github.io"
            for article in articles:
                item = demoItem()
                # .//当前节点下所有符合的节点
                url = article.xpath('.//a[@class="post-title-link"]/@href').extract()[0]
                item['url'] = domain_url + url
                # /text()是标签内容
                item['name'] = article.xpath('.//a[@class="post-title-link"]/text()').extract()[0]
                item['date'] = article.xpath('.//time/text()').extract()[0].strip()
                # 如果不是嵌套 直接 yield  item
                # yield item

                items.append(item)

        for item in items:
                # scrapy 在不同的抓取级别的Request之间传递参数的办法，
                # 下面的范例中，parse()通过meat传递给了parse_more()参数item，
                # 这样就可以再parse_more()抓取完成所有的数据后一次返回
            yield Request(item['url'], meta={'item': item}, callback=self.parse_more, dont_filter=True)

            # url = site.xpath('CONTENTLINK/text()')
            # if url.extract():
            #     item['url'] = url.extract()[0]
            #     items.append(item)



    def parse_more(self,response):
        item = response.meta['item']
        # name = response.xpath('//CONTENT[1]/text()')
        # author = response.xpath('//LCONTENT/text()')
        # item['name'] = name.extract()[0]

        description = response.xpath('//div[@class="post-description"]/text()').extract()
        if description:
            item['description'] = description[0].strip()
        else:
            item['description'] = ""

            # 判断HTML标签内容为空，跳过空的
        # if author.extract():
        #     item['author'] =  author.extract()[0]
        # item["url_id"] = response.xpath('//div[@class="main"]/div[@class="info"]/table[@class="table-1"]/tr[2]/td/text()').extract()[0]
        # site = response.xpath('//div[@class="detail"]/div[@class="info"]/table[@class="table-1"]')
        # item["url_name"] = site.xpath('tr[1]/td/text()').extract()[0]
        # item['url_enterprise'] = site.xpath('tr[2]/td/a[1]/text()').extract()[0]
        # item['url_function'] = site.xpath('tr[3]/td/text()').extract()[0]
        # item['url_usage'] = site.xpath('tr[4]/td/text()').extract()[0]

        yield item