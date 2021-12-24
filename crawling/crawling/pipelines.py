from estates.models import Estate
from estates.models import ImageList
from unidecode import unidecode


def clean_title(param):
    return param


def clean_price(param):
    return int(unidecode(param).replace(",", ""))


def clean_area(param):
    return int(unidecode(param).replace(",", ""))


def clean_feature(param):
    if param == "دارد":
        return True
    return False


def clean_year(param):
    return param


def clean_estate_type(param):
    return param


def clean_use_type(param):
    return param


def clean_region(param):
    return param


class CrawlingPipeline(object):
    def process_item(self, item, spider):
        model = {}
        model["title"] = clean_title(item["title"])
        if "price" in item:
            model["price"] = clean_price(item["price"])
        if "area" in item:
            model["area"] = clean_area(item["area"])
        # Todo: change text to numeric
        if "rooms" in item:
            model["rooms"] = clean_title(item["rooms"])
        if "parking" in item:
            model["parking"] = clean_feature(item["parking"])
        if "year" in item:
            model["year"] = clean_year(item["year"])
        if "store" in item:
            model["store"] = clean_feature(item["store"])
        if "ppm" in item:
            model["ppm"] = clean_price(item["ppm"])
        if "elevator" in item:
            model["elevator"] = clean_feature(item["elevator"])
        if "estate_type" in item:
            model["estate_type"] = clean_estate_type(item["estate_type"])
        if "use_type" in item:
            model["use_type"] = clean_use_type(item["use_type"])
        if "region" in item:
            model["region"] = clean_region(item["region"])
        if "image_url" in item:
            model["image_url"] = clean_title(item["image_url"])
        # price = clean_title(item["price"])
        # area = clean_title(item["area"])
        # critics_consensus = clean_critics_consensus(item["critics_consensus"])
        # average_grade = clean_average_grade(item["average_grade"])
        # poster = clean_poster(item["images"])
        # amount_reviews = clean_amount_reviews(item["amount_reviews"])
        # approval_percentage = clean_approval_percentage(item["approval_percentage"])

        Estate.objects.create(**model)

        return item
