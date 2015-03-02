from scrapy.spider import Spider
from scrapy.selector import Selector
from yelp_crawler.items import YelpItem
import csv

class YelpSpider(Spider):
	name = "yelp"
	allowed_domain = ["yelp.com"]

	def get_start_urls():
		url_list = {}
		start_urls = []
		with open('/Users/lily/workspace/crwaler/summer_2014_research/mallsdata.csv', 'rb') as csvfile:
		   spamreader = csv.reader(csvfile, delimiter=',')
		   for row in spamreader:
			   mall_list = row[7]
			   state = row[1]
			   for mall in mall_list.split("|"):
			   		mall = mall.strip()
			   		url_list[mall] = state
			   		start_urls.append("http://www.yelp.com/search?find_loc=" + state + "&ns=1&find_desc=" + mall)
			   		print start_urls
		return start_urls



	start_urls = get_start_urls()

	def parse(self, response):
		sel = Selector(response)
		stores = sel.xpath('//div[@data-key="1"]')
		# first_store = stores[0]
		items = []
		for first_store in stores:
			item = YelpItem()
				# compare name between the search one and blow
				# use regular expression to filter the name
				# prada vs prada ny
			item['name'] = first_store.xpath('.//a[@class="biz-name"]/span/text()').extract()
			item['address'] = first_store.xpath('.//address/text()').extract()
				#@todo todo just left 3.5 use pace to split the string
			item['rate'] = first_store.xpath('.//div[@class="rating-large"]/i/@title').extract()
				#@todo replace $$$$ with numbers
			item['price_range'] = first_store.xpath('.//div[@class="price-category"]/span/span/text()').extract()
				#@todo concat retuen array as a string 
			item['category'] = first_store.xpath('.//span[@class="category-str-list"]/a/text()').extract()
			item['url'] = first_store.xpath('.//a[@class="biz-name"]/@href').extract()
			items.append(item)
		return items

	