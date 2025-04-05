import re
from collections.abc import Generator
from typing import Any, Self

import scrapy
from parsel import SelectorList
from scrapy.http.response import Response

from src.logs import print_info


class PortalInmobiliarioScrapper(scrapy.Spider):
    name = "portal-inmobiliario-scrapper"
    start_urls = [  # noqa: RUF012
        "https://www.portalinmobiliario.com/arriendo/departamento/providencia-metropolitana/_PublishedToday_YES",
    ]
    CARD_SELECTOR_CLASS = ".ui-search-result__wrapper"
    TYPE_PROPERTY_OFFERING = ".poly-component__headline"
    PROPERTY_PRICE_CURRENCY = ".andes-money-amount__currency-symbol"
    # If property is in UF then can contain cents
    PROPERTY_PRICE_VALUE = ".andes-money-amount__fraction"
    PROPERTY_PRICE_VALUE_CENTS = ".andes-money-amount__cents"
    PROPERTY_FEATURES = ".poly-attributes-list"
    CARD_TITLE = ".poly-component__title"
    PROPERTY_LOCATION = ".poly-component__location"

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.portalinmobiliario.com/",
        }

        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, encoding="utf-8")

    def parse(self: Self, response: Response) -> Generator[dict[str, Any]]:
        print_info("Starting scrapper")

        for card in response.css(self.CARD_SELECTOR_CLASS):
            title = card.css(f"{self.CARD_TITLE}::text").extract_first()
            offering = card.css(f"{self.TYPE_PROPERTY_OFFERING}::text").extract_first()
            currency = card.css(f"{self.PROPERTY_PRICE_CURRENCY}::text").extract_first()
            price = card.css(f"{self.PROPERTY_PRICE_VALUE}::text").extract_first()
            features = card.css(f"{self.PROPERTY_FEATURES}")
            property_location = card.css(f"{self.PROPERTY_LOCATION}::text").extract_first()
            property_url = card.css("a::attr(href)").extract_first()

            print_info(f"Extracting {title}")

            yield {
                "offering": offering,
                "title": title,
                "currency": currency,
                "price": self.extract_number(text=price),
                **self.parse_property_features(props=features),
                "location": property_location,
                "url": property_url,
            }

    def parse_property_features(
        self: Self,
        props: SelectorList[Any],
    ) -> dict[str, int | None]:
        list_item_selector = "li"
        items = props.css(f"{list_item_selector}::text").getall()

        items = dict(enumerate(iterable=items))

        return {
            "bedrooms": self.extract_number(text=items.get(0)),
            "baths": self.extract_number(text=items.get(1)),
            "space": self.extract_number(text=items.get(2)),
        }

    def extract_number(
        self: Self,
        text: str | None,
        default: int | None = None,
    ) -> int | None:
        if text is None:
            return default

        text_clean = text.replace(".", "")
        match = re.search(pattern=r"\d+", string=text_clean)
        if match:
            number = int(match.group())
            return number

        return default
