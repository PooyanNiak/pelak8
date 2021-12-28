import scrapy
from crawling.items import EstateItem
from scrapy.spiders import CrawlSpider

translateDict = {
    "سن بنا": "year",
    "رهن": "mortgage",
    "پارکینگ": "parking",
    "قیمت": "price",
    "نوع ملک": "estate_type",
    "نوع کاربری": "use_type",
    "اجاره": "rent",
    "تعداد اتاق": "rooms",
    "قابلیت تبدیل مبلغ رهن و اجاره": "convertable",
    "انباری": "store",
    "مساحت": "area",
    "متراژ": "area",
    "آسانسور": "elevator",
    "قیمت هر متر": "ppm",
}


class SheypoorSpider(CrawlSpider):

    name = "sheypoor"
    allowed_domains = ["www.sheypoor.com"]

    def start_requests(self):
        urls = [
            "https://www.sheypoor.com/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/%D8%A7%D9%85%D9%84%D8%A7%DA%A9",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        rows = response.xpath('//div[@class="content"]//h2/a/@href').extract()
        for row in rows:
            link = row
            yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        i = EstateItem()
        i["title"] = response.xpath(
            '//section[@id="item-details"]//h1/text()', first=True
        ).get()
        price = response.xpath('//*[@class="item-price"]/node()', first=True).get()
        if price:
            if "strong" in price:
                i["price"] = response.xpath(
                    '//*[@class="item-price"]//strong/text()', first=True
                ).get()
            else:
                i["price"] = response.xpath(
                    '//*[@class="item-price"]/text()', first=True
                ).get()
        i["region"] = response.xpath(
            '//*[@id="item-details"]//span[@class="small-text"]/text()', first=True
        ).get()
        image_url = response.xpath(
            '//*[@class="slideshow "]//img/@src', first=True
        ).get()
        if image_url:
            i["image_url"] = response.xpath(
                '//*[@class="slideshow "]//img/@src', first=True
            ).get()
        i["url"] = response.url
        i["source"] = "sheypoor"
        features = response.xpath("//tr")
        for feature in features:
            label = feature.css("th ::text")[0].get()
            value = feature.css("td ::text")[0].get()
            if label in translateDict.keys():
                print("label: ", label, "value", value)
                i[translateDict[label]] = value.strip()
            elif label:
                print("new label: ", label)
        # i["average_grade"] = response.css("#js-rotten-count ::text").extract()[1]
        # i["amount_reviews"] = response.css(
        #     ".mop-ratings-wrap__text--small ::text"
        # ).extract()[1]
        # i["approval_percentage"] = response.css(
        #     ".mop-ratings-wrap__percentage ::text"
        # ).extract_first()
        # i["image_urls"] = response.css(".posterImage ::attr(data-src)").extract()
        return i
