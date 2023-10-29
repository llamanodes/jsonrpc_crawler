from playwright.async_api import (
    Request as PlaywrightRequest,
    Response as PlaywrightResponse,
)
from scrapy_playwright.page import PageMethod
from scrapy.http import HtmlResponse
import scrapy
import json


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
            # errback=self.errback,
            playwright=True,
            playwright_include_page=False,
            playwright_page_event_handlers={
                "request": "handle_request",
            },
            playwright_page_methods=[
                # TODO: what should we do? inject some javascript to connect a mock wallet/provider?
                PageMethod('wait_for_load_state', state='networkidle', timeout=60 * 1000),
            ],
        )

        meta.update(**kwargs)

        return meta

    def start_requests(self):
        yield scrapy.Request(
            "https://curve.fi/#/ethereum/pools/3pool/deposit", meta=self.scrapy_meta(playwright_context="curve")
        )
        # yield scrapy.Request(
        #     "https://www.convexfinance.com",
        #     meta=self.scrapy_meta(playwright_context="convex"),
        # )

    def parse(self, response: HtmlResponse):
        # 'response' contains the page as seen by the browser

        if not response.status != 200:
            return

        print(response.headers)

        if response.headers["content-type"] != "text/html":
            return

        try:
            # TODO: does `response` work here or do we need to parse the `page`
            links = response.xpath("//a[@href]/@href").getall()
        except Exception:
            # TODO: just the one type of exception
            return

        for link in links:
            if link in self.handled:
                continue

            self.handled.add(link)

            # TODO: do some extra filtering on these links? i think scrapy handles enough for us with self.allowed_domains
            self.logger.debug("following link on %s: %s", response.request.url, link)

            follow_meta = self.scrapy_meta(
                playwright_context=response.meta["playwright_context"]
            )

            # TODO: follow links once loading one page works fully
            # TODO: following links should be optional
            yield response.follow(link, callback=self.parse, meta=follow_meta)

    def handle_request(self, request: PlaywrightRequest) -> None:
        if request.method == "POST" and request.resource_type in ["fetch", "xhr"] and "jsonrpc" in request.post_data:
            try:
                data = request.post_data_json
            except Exception:
                # TODO: just the one type of exception
                pass
            else:
                # TODO: include request.url in this so that we can tell what rpc/chain it is going to
                # TODO: should this yield an `Item`?
                # TODO: attach referer header
                print(json.dumps(dict(url=request.url, data=data)))
                return

            self.logger.debug(
                f"non-jsonrpc seen: {request.resource_type, request.url, request.method, request.post_data}"
            )
        else:
            # TODO: this is too verbose
            # self.logger.debug(
            #     f"request ignored: {request.resource_type, request.url, request.method}"
            # )
            pass

    async def errback(self, failure):
        if page := failure.request.meta.get("playwright_page"):
            await page.close()
