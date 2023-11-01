from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from db.connect import Database
from parser.infer import infer
import json

equal = {
    "U.S.": "American",
    "Southern": "American",
    "Southwestern": "American",
    "New England": "American",
    "Tex Mex": "Mexican Inspired",
    "English": "British",
}
blacklist = ["Inspired", "World"]


class AllRecipesSpider(CrawlSpider):
    name = "allrecipes"
    start_urls = ["https://www.allrecipes.com/"]
    rules = (
        Rule(
            LinkExtractor(
                allow_domains="www.allrecipes.com", allow=["/recipes/", "/recipe/"]
            ),
            callback="parse",
            follow=True,
        ),
    )
    db = Database().get_client()

    def parse(self, response):
        # only crawl recipes with labeled cuisine
        # parse: find the embedded recipe schema
        if "/recipe/" not in response.url:
            return
        try:
            schema = json.loads(
                response.css("#allrecipes-schema_1-0::text").extract()[0]
            )[0]
        except:
            self.logger.error(
                "Couldn't find recipe schema on page <" + response.url + ">"
            )
            return
        if "Recipe" not in schema["@type"] or "recipeCuisine" not in schema:
            return

        # filter cuisines
        cuisines = set()
        for cuisine in schema["recipeCuisine"]:
            # "__ Inspired" = __ and American
            inspired = cuisine.replace(" Inspired", "")
            if inspired != cuisine:
                cuisines.add("American")
                cuisine = inspired

            # convert equivalent cuisines (U.S. --> American)
            if cuisine in equal:
                cuisine = equal[cuisine]

            if cuisine not in blacklist:
                cuisines.add(cuisine)

        # insert recipe into database
        self.db.insert_one(
            {
                "url": response.url,
                "name": schema["headline"],
                "cuisine": list(cuisines),
                # "ingredients": schema["recipeIngredient"],
                "ner": infer(schema["recipeIngredient"])["ingredients"],
            }
        )
