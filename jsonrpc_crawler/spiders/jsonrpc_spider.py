import scrapy


class JsonrpcSpider(scrapy.Spider):
    name = "jsonrpc"
    custom_settings = {
        "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": None,  # needed to keep playwright headers
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        # "PLAYWRIGHT_CDP_URL": "http://localhost:9222",
    }

    def start_requests(self):
        yield scrapy.Request("https://curve.fi", meta={"playwright": True})

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        return {"url": response.url}
