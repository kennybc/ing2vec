from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from db.connect import Database
from parser.infer import infer
import json


class AllRecipesSpider(CrawlSpider):
    name = "allrecipes"
    start_urls = ["https://www.allrecipes.com/"]
    rules = (Rule(LinkExtractor(allow_domains="www.allrecipes.com", allow=["/recipes/", "/recipe/"]),
             callback="parse", follow=True),)
    db = Database().get_client()

    def parse(self, response):

        # crawl but do not parse recipe category pages
        # parse: find the embedded recipe schema
        if "/recipe/" not in response.url:
            return
        try:
            schema = json.loads(response.css(
                "#allrecipes-schema_1-0::text").extract()[0])[0]
        except:
            self.logger.error(
                "Couldn't find recipe schema on page <" + response.url + ">")
            return
        if "Recipe" not in schema["@type"] or "/recipe/" not in response.url:
            return
        
        # insert recipe into database
        self.db.insert_one({
            "url": response.url,
            "name": schema["headline"],
            "ingredients": schema["recipeIngredient"],
            "ner": infer(schema["recipeIngredient"])["ingredients"]
        })
