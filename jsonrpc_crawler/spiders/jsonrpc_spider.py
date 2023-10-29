from playwright.async_api import (
    Request as PlaywrightRequest,
    Response as PlaywrightResponse,
)
import scrapy
import json

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
    handled = set()

    def scrapy_meta(self, **kwargs):
        meta = dict(
            errback=self.errback,
            playwright=True,
            playwright_include_page=True,
            playwright_page_event_handlers={
                "request": "handle_request",
                # "response": "handle_response",  # TODO: do we want this?
            },
            playwright_page_coroutines=[
                # TODO: what should we do? inject some javascript to connect a mock wallet/provider?
                # PageCoroutine("wait_for_timeout", 30 * 1000)
            ],
        )

        meta.update(**kwargs)

        return meta

    def start_requests(self):
        yield scrapy.Request(
            "https://curve.fi", meta=self.scrapy_meta(playwright_context="curve")
        )
        yield scrapy.Request(
            "https://www.convexfinance.com",
            meta=self.scrapy_meta(playwright_context="convex"),
        )

    async def parse(self, response: PlaywrightResponse):
        # 'response' contains the page as seen by the browser

        # TODO: skip scraping non-html pages
        # if response.content_type != "text/html":
        #     return

        # playwright_page is set when request.meta.playwright == True
        page = response.meta["playwright_page"]

        # TODO: if page is set, wait for the page to load? (it isn't always set. why?)

        try:
            # TODO: does `response` work here or do we need to parse the `page`
            links = response.xpath("//a[@href]/@href").getall()
        except Exception:
            # TODO: just the one type of exception
            return

        yield {"url": response.url, "page": page}

        for link in links:
            if link in self.handled:
                continue

            if link.endswith(".js") or link.endswith(".png"):
                continue

            self.handled.add(link)

            # TODO: do some extra filtering on these links? i think scrapy handles enough for us with self.allowed_domains
            self.logger.debug("following link on %s: %s", response.request.url, link)

            follow_meta = self.scrapy_meta(
                playwright_context=response.meta["playwright_context"]
            )

            yield response.follow(link, callback=self.parse, meta=follow_meta)

    async def handle_request(self, request: PlaywrightRequest) -> None:
        # self.logger.debug(
        #     f"request seen: {request.resource_type, request.url, request.method}"
        # )

        if request.method == "POST" and (
            request.resource_type == "fetch" or request.resource_type == "xhr"
        ):
            try:
                data = request.post_data_json
            except Exception:
                # TODO: just the one type of exception
                return

            if data is None:
                return

            if "jsonrpc" in data:
                # TODO: include request.url in this so that we can tell what rpc/chain it is going to
                # TODO: should this yield an `Item`?
                print(json.dumps(dict(url=request.url, data=data)))

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
