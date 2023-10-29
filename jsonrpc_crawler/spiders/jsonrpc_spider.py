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
            # TODO: we probably need to include_page so that we can click all the things that aren't actually links
            # playwright_include_page=False,

            playwright_include_page=True,
            errback=self.errback,

            playwright=True,
            playwright_page_event_handlers={
                "request": "handle_request",
            },
            playwright_page_methods=[
                # attach our crawler wallet and provider
                PageMethod('add_init_script', path='preload.js'),
                # TODO: if there is a "connect wallet" button on the page, click it
                # TODO: timeout on this is probably a good idea, but it seems to throw an exception instead of just exiting quietly
                PageMethod('wait_for_load_state', state='networkidle', timeout=30 * 1000),
            ],
        )

        meta.update(**kwargs)

        return meta

    def start_requests(self):
        yield scrapy.Request(
            "https://curve.fi/", meta=self.scrapy_meta(playwright_context="curve")
        )
        yield scrapy.Request(
            "https://classic.curve.fi/", meta=self.scrapy_meta(playwright_context="curve classic")
        )
        yield scrapy.Request(
            "https://curve.fi/#/ethereum/pools/3pool/deposit", meta=self.scrapy_meta(playwright_context="curve 3pool")
        )
        yield scrapy.Request(
            "https://www.convexfinance.com",
            meta=self.scrapy_meta(playwright_context="convex"),
        )

    async def parse(self, response: HtmlResponse):
        page = response.meta["playwright_page"]

        # TODO: gather all the things that aren't actually links but still point to other pages

        await page.close()

        if response.status != 200:
            return

        if not response.headers[b'Content-Type'].startswith(b"text/html"):
            self.logger.debug("skipping non html: %s", response.url)
            return

        try:
            # TODO: does `response` work here or do we need to parse the `page`
            links = response.xpath("//a[@href]/@href").getall()
        except Exception:
            # TODO: just the one type of exception
            links = []

        # TODO: `screenshot = await page.screenshot(path="example.png", full_page=True)`

        return

        for link in links:
            if link in self.handled:
                continue

            # TODO: do this less fragile
            # TODO: skip images, css, js, xml, etc
            if "gov.curve.fi" in link or "api.curve.fi" in link or "github.com" in link:
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
                request_json = request.post_data_json
            except Exception:
                # TODO: catch just the one type of exception
                pass
            else:
                # TODO: include request.url in this so that we can tell what rpc/chain it is going to
                # TODO: should this yield an `Item`?
                # TODO: attach referer header
                print(json.dumps(dict(url=request.url, request=request_json)))
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
        page = failure.request.meta["playwright_page"]
        await page.close()
