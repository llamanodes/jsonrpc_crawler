from playwright.async_api import Request as PlaywrightRequest, Response as PlaywrightResponse
import scrapy

# from scrapy_playwright.page import PageCoroutine

class JsonrpcSpider(scrapy.Spider):
    name = "jsonrpc"
    allowed_domains = ["curve.fi", "convexfinance.com"]
    custom_settings = {
        "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": None,  # needed to keep playwright headers
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    def scrapy_meta(self, **kwargs):
        meta = dict(
            errback = self.errback,
            playwright = True,
            playwright_include_page = True,
            playwright_page_event_handlers = {
                "request": "handle_request",
                #"response": "handle_response",  # TODO: do we want this?
            },
            playwright_page_coroutines = [
                # TODO: what should we do? inject some javascript to connect a mock wallet/provider?
                # PageCoroutine("wait_for_timeout", 30 * 1000)
            ],
        )

        meta.update(**kwargs)

        return meta

    def start_requests(self):
        yield scrapy.Request(
            "https://curve.fi",
            meta=self.scrapy_meta(playwright_context= "curve")
        )
        yield scrapy.Request(
            "https://dao.curve.fi",
            meta=self.scrapy_meta(playwright_context= "curve dao")
        )
        yield scrapy.Request(
            "https://www.convexfinance.com",
            meta=self.scrapy_meta(playwright_context= "convex")
        )

    async def parse(self, response: PlaywrightResponse):
        # 'response' contains the page as seen by the browser

        page = response.meta["playwright_page"]

        return {"url": response.url, "page": page}

    async def handle_request(self, request: PlaywrightRequest) -> None:
        # self.logger.debug(
        #     f"request seen: {request.resource_type, request.url, request.method}"
        # )

        if request.resource_type == "fetch" and request.method == "POST":
            self.logger.info("fetch POST request")

            data = request.post_data_json

            if data is None:
                return

            if "jsonrpc" in data:
                print(data)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
 