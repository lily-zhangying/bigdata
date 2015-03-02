from scrapy.spider import Spider
from scrapy.selector import Selector
from yelp_crawler.items import YelpItem

class YelpSpider(Spider):
	name = "yelp"

	allowed_domain = ["yelp.com"]
	start_urls = [
		"http://www.yelp.com/search?find_loc=nyc&ns=1&find_desc=chanel",
		"http://www.yelp.com/search?find_loc=nyc&ns=1&find_desc=prada",
		"http://www.yelp.com/search?find_loc=nyc&ns=1&find_desc=enzo",
		"http://www.yelp.com/search?find_loc=nyc&ns=1&find_desc=H&M"
	]

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
				# todo just left 3.5 use pace to split the string
			item['rate'] = first_store.xpath('.//div[@class="rating-large"]/i/@title').extract()
				# replace $$$$ with numbers
			item['price_range'] = first_store.xpath('.//div[@class="price-category"]/span/span/text()').extract()
				# concat retuen array as a string 
			item['category'] = first_store.xpath('.//span[@class="category-str-list"]/a/text()').extract()
			item['url'] = first_store.xpath('.//a[@class="biz-name"]/@href').extract()
			items.append(item)
		return items

