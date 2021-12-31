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


class SheypoorSpider(CrawlSpider):

    name = "iranfile"
    allowed_domains = []
    global cookie
    cookie = "7516586128311E5D62B73F18CF33BE6325C6B12063EFA5604F2B411491710486FA5EF26292E83145066753B2131920BFE92D86505A9EFB14395CF6CF2CECBB4CD5C05B650E393F8B62B6884B5F7312F018F747B256EDB65D8ADD74E81560741A5F7A22C48C55B6DBB4AE2705C2AC410BC03C0CCA"

    def start_requests(self):
        urls = [
            "https://iranfile.net/search.aspx",
        ]
        for url in urls:
            yield scrapy.Request(
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
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage");
        chrome_options.add_argument("--remote-debugging-port=9222")  # this

        chrome_options.add_argument("--disable-dev-shm-using")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        # self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.get(response.url)

        self.driver.add_cookie(
            {
                "name": ".ASPXAUTH",
                "value": "7516586128311E5D62B73F18CF33BE6325C6B12063EFA5604F2B411491710486FA5EF26292E83145066753B2131920BFE92D86505A9EFB14395CF6CF2CECBB4CD5C05B650E393F8B62B6884B5F7312F018F747B256EDB65D8ADD74E81560741A5F7A22C48C55B6DBB4AE2705C2AC410BC03C0CCA",
            }
        )
        searchBtn = self.driver.find_element_by_xpath('//button[@id="btnSearchM"]')
        searchBtn.click()
        time.sleep(15)
        rows = []
        container = self.driver.find_elements_by_xpath(
            '//ul[@id="searchResultM"]//button'
        )
        print("lennnnnnnnnnnnnnnnnnnnnnnnn", len(container))
        rows.extend(
            self.driver.find_elements_by_xpath('//button[@class="list-group-item"]//a')
        )
        rows.extend(
            self.driver.find_elements_by_xpath(
                '//button[@class="list-group-item row_striped"]//a'
            )
        )
        # for row in container:
        #     self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
        #     rows.extend(
        #         self.driver.find_elements_by_xpath(
        #             '//ul[@id="searchResultM"]//button[@class="list-group-item"]//a'
        #         )
        #     )
        #     rows.extend(
        #         self.driver.find_elements_by_xpath(
        #             '//ul[@id="searchResultM"]//button[@class="list-group-item row_striped"]//a'
        #         )
        #     )
        # print(
        #     "******************************* rows Num : ",
        #     len(rows),
        #     " ************************************",
        # )
        # uniqueRows = list(dict.fromkeys(rows))
        # print(
        #     "******************************* uniques Num : ",
        #     len(uniqueRows),
        #     " ************************************",
        # )
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
        time.sleep(15)
        region = self.driver.find_elements_by_xpath('//*[@id="lbRegion"]')[0].text
        title_type = self.driver.find_elements_by_xpath("//h4[@id='lbTitle']")[0].text
        date = self.driver.find_elements_by_xpath('//*[@id="lbIranDate"]')[0].text
        owner = self.driver.find_elements_by_xpath('//*[@id="lbOwner"]')[0].text
        phone = self.driver.find_elements_by_xpath('//*[@id="lbTel"]//a')
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

        i["title"] = title_type
        if region:
            i["region"] = region
        if date:
            i["date"] = date
        if owner:
            i["owner"] = owner
        if phone:
            i["phone"] = phone[0].get_attribute("href")
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
