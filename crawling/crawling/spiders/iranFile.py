import scrapy
from scrapy_selenium import SeleniumRequest
from crawling.items import EstateItem
from scrapy.spiders import CrawlSpider
from scrapy.http import FormRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
from selenium.webdriver.remote.remote_connection import LOGGER, logging

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
SELENIUM_IS_HEADLESS = False


class SheypoorSpider(CrawlSpider):

    name = "iranfile"
    allowed_domains = []
    global cookie
    cookie = "2E0B6ABD34199914270BE2B594697FBF7ACCD84A7D3A7D206C96E5D1D3330B6C3DBBE19F47FE32C967C0CACEFD43B3B7B9E1BAD281C3E96F60AC4EC8C8C4D4D023B7D969A43146836CF2CB09719D93BAAFFA5ED8C57887174BDC11CE1B9027C2F37025EADA6C181A3A1BD0FD4076C062270C1F25"

    def start_requests(self):
        urls = [
            "https://iranfile.net/search.aspx",
        ]
        for url in urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                cookies=[{"name": ".ASPXAUTH", "value": cookie,}],
            )

    # def start_requests(self):
    #     return [
    #         FormRequest(
    #             "https://iranfile.net/Login.aspx",
    #             formdata={
    #                 "ctl00$ContentPlaceHolderContent$userID": "iranFile",
    #                 "ctl00$ContentPlaceHolderContent$password": "12345678",
    #             },
    #             callback=self.start_links,
    #         )
    #     ]

    def parse(self, response):
        loginFailed = response.xpath(
            '//a[@href="/login.aspx?ReturnUrl=%2fsearch.aspx"]'
        ).extract()
        print("loginFailed", loginFailed)
        loginSuccess = response.xpath(
            '//ul[@class="nav navbar-nav"]//li//a[@class="dropdown-toggle"]'
        ).extract()
        print("loginSuccess", loginSuccess)
        LOGGER.setLevel(logging.WARNING)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
        }
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.get(response.url)
        searchBtn = self.driver.find_element_by_xpath('//button[@id="btnSearchM"]')
        searchBtn.click()
        time.sleep(15)
        rows = self.driver.find_elements_by_xpath(
            '//button[@class="list-group-item row_striped"]//a'
        )
        self.driver.add_cookie(
            {
                "name": ".ASPXAUTH",
                "value": "2E0B6ABD34199914270BE2B594697FBF7ACCD84A7D3A7D206C96E5D1D3330B6C3DBBE19F47FE32C967C0CACEFD43B3B7B9E1BAD281C3E96F60AC4EC8C8C4D4D023B7D969A43146836CF2CB09719D93BAAFFA5ED8C57887174BDC11CE1B9027C2F37025EADA6C181A3A1BD0FD4076C062270C1F25",
            }
        )
        for row in rows:
            print("row ********************************", row.get_attribute("href"))
            if "fs.aspx" in row.get_attribute("href"):
                # response = self.driver.get(row.get_attribute("href"))
                # self.parse_item(response)
                yield SeleniumRequest(
                    url=str(row.get_attribute("href")),
                    callback=self.parse_item,
                    cookies=[{"name": ".ASPXAUTH", "value": cookie,}],
                )
            else:
                print(
                    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& Else &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                )

    def parse_item(self, response):
        i = EstateItem()
        self.driver.get(response.url)
        time.sleep(5)
        region = self.driver.find_elements_by_xpath('//*[@id="lbRegion"]')[0].text
        title_type = self.driver.find_elements_by_xpath("//h4[@id='lbTitle']")[0].text
        title_name = self.driver.find_elements_by_xpath("//*[@id='lbTitle']/span")[
            0
        ].text
        date = self.driver.find_elements_by_xpath('//*[@id="lbIranDate"]')[0].text
        owner = self.driver.find_elements_by_xpath('//*[@id="lbOwner"]')[0].text
        phone = self.driver.find_elements_by_xpath('//*[@id="lbTel"]//a')[
            0
        ].get_attribute("href")
        price = self.driver.find_elements_by_xpath('//*[@id="lbTotalPrice"]')[0].text
        rooms = self.driver.find_elements_by_xpath('//*[@id="lbFloorNo"]')[0].text
        ppm = self.driver.find_elements_by_xpath('//*[@id="lbUnitPrice"]')[0].text
        area = self.driver.find_elements_by_xpath('//*[@id="lbArea"]')[0].text
        direction = self.driver.find_elements_by_xpath('//*[@id="lbDirection"]')[0].text
        floor = self.driver.find_elements_by_xpath('//*[@id="lbUnitNo"]')[0].text
        address = self.driver.find_elements_by_xpath('//*[@id="lbAddress"]')[0].text
        description = self.driver.find_elements_by_xpath('//*[@id="lbComment"]')[0].text
        balcon = self.driver.find_elements_by_xpath('//*[@id="lbBalcon11"]')[0].text
        parking = self.driver.find_elements_by_xpath('//*[@id="lbParking1"]')[0].text
        store = self.driver.find_elements_by_xpath('//*[@id="lbAnbari1"]')[0].text

        features = self.driver.find_elements_by_xpath(
            '//*[@id="divEquipment"]/div//div'
        )
        equipments = ""
        if features:
            for feature in features:
                equipments += "," + feature.text
        print("feature: ", equipments)

        i["title"] = title_type + " " + title_name
        if region:
            i["region"] = region
        if date:
            i["date"] = date
        if owner:
            i["owner"] = owner
        if phone:
            i["phone"] = phone
        if price:
            i["price"] = price
        if rooms:
            i["rooms"] = rooms
        if ppm:
            i["ppm"] = ppm
        if area:
            i["area"] = area
        if direction:
            i["direction"] = direction
        if address:
            i["address"] = address
        if description:
            i["description"] = description
        if floor:
            i["floor"] = floor
        if len(equipments):
            i["equipments"] = equipments
        if parking:
            i["parking"] = parking
        if balcon:
            i["balcon"] = balcon
        if store:
            i["store"] = store
        i["url"] = response.url
        i["source"] = "iranfile"
        # i["title"] = response.xpath('//h4[@id="#lbTitle"]/text()', first=True).get()
        # price = response.xpath('//*[@class="item-price"]/node()', first=True).get()
        # if price:
        #     if "strong" in price:
        #         i["price"] = response.xpath(
        #             '//*[@class="item-price"]//strong/text()', first=True
        #         ).get()
        #     else:
        #         i["price"] = response.xpath(
        #             '//*[@class="item-price"]/text()', first=True
        #         ).get()
        # i["region"] = response.xpath(
        #     '//*[@id="item-details"]//span[@class="small-text"]/text()', first=True
        # ).get()
        # image_url = response.xpath(
        #     '//*[@class="slideshow "]//img/@src', first=True
        # ).get()
        # if image_url:
        #     i["image_url"] = response.xpath(
        #         '//*[@class="slideshow "]//img/@src', first=True
        #     ).get()

        # features = response.xpath("//tr")
        # for feature in features:
        #     label = feature.css("th ::text")[0].get()
        #     value = feature.css("td ::text")[0].get()
        #     if label in translateDict.keys():
        #         print("label: ", label, "value", value)
        #         i[translateDict[label]] = value.strip()
        #     elif label:
        #         print("new label: ", label)
        # i["average_grade"] = response.css("#js-rotten-count ::text").extract()[1]
        # i["amount_reviews"] = response.css(
        #     ".mop-ratings-wrap__text--small ::text"
        # ).extract()[1]
        # i["approval_percentage"] = response.css(
        #     ".mop-ratings-wrap__percentage ::text"
        # ).extract_first()
        # i["image_urls"] = response.css(".posterImage ::attr(data-src)").extract()
        return i
