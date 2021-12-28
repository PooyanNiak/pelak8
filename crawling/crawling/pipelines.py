from estates.models import Estate
from estates.models import ImageList
from unidecode import unidecode


def clean_title(param):
    return param


def clean_price(param):
    # numbers = [int(word) for word in param.split() if word.isdigit()]
    return int(param.replace(",", ""))


def clean_area(param):
    # numbers = [int(word) for word in param.split() if word.isdigit()]
    return int(param.replace(",", ""))


def clean_feature(param):
    if param != "ندارد":
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


def clean_phone(param):
    return param


class CrawlingPipeline(object):
    def process_item(self, item, spider):
        model = {}
        if "title" in item:
            model["title"] = clean_title(item["title"])
        else:
            model["title"] = "test"
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
        if "balcon" in item:
            model["balcon"] = clean_feature(item["balcon"])
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
        if "phone" in item:
            model["phone"] = clean_phone(item["phone"])
        if "floor" in item:
            model["floor"] = clean_phone(item["floor"])
        if "direction" in item:
            model["direction"] = clean_phone(item["direction"])
        if "owner" in item:
            model["owner"] = clean_phone(item["owner"])
        if "date" in item:
            model["date"] = clean_phone(item["date"])
        if "address" in item:
            model["address"] = clean_title(item["address"])
        if "description" in item:
            model["description"] = clean_title(item["description"])
        if "url" in item:
            model["url"] = clean_title(item["url"])
        if "source" in item:
            model["source"] = clean_title(item["source"])
        if "equipments" in item:
            model["equipments"] = clean_title(item["equipments"])
        # critics_consensus = clean_critics_consensus(item["critics_consensus"])
        # average_grade = clean_average_grade(item["average_grade"])
        # poster = clean_poster(item["images"])
        # amount_reviews = clean_amount_reviews(item["amount_reviews"])
        # approval_percentage = clean_approval_percentage(item["approval_percentage"])

        Estate.objects.create(**model)

        return item
