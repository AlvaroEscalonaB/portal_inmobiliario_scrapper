from typing import Any

from scrapy.crawler import CrawlerProcess

from src.logs import print_df_as_table, print_info
from src.portal_crawler import PortalInmobiliarioScrapper
from src.summary import run_summary_analysis

results: list[Any] = []  # Store extracted data


if __name__ == "__main__":
    from pathlib import Path

    path_to_save_crawler = Path.cwd() / "outputs" / "output.json"

    process = CrawlerProcess(
        settings={
            "FEEDS": {
                str(path_to_save_crawler): {
                    "format": "json",
                    "overwrite": True,
                },
            }
        }
    )
    process.crawl(crawler_or_spidercls=PortalInmobiliarioScrapper)
    process.start()

    print_info("Finish of crawler and output generated")
    df = run_summary_analysis(path_to_save_crawler)
    selected_cols = ["price", "bedrooms", "baths", "url"]
    print_df_as_table(df[selected_cols])
