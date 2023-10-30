# jsonrpc_crawler
crawl dapps and extract all their jsonrpc requests

## Usage

Installation:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Run the spider:

```
scrapy crawl jsonrpc | jq -c .request | versus https://ethereum.llamarpc.com https://rpc.ankr.com/eth https://eth.drpc.org https://eth.merkle.io https://eth.meowrpc.com https://1rpc.io/eth
```

Example output starts with a bunch of debug logs that don't matter so much.

```
2023-10-29 21:49:57 [scrapy.utils.log] INFO: Scrapy 2.11.0 started (bot: jsonrpc_crawler)
2023-10-29 21:49:57 [scrapy.utils.log] INFO: Versions: lxml 4.9.3.0, libxml2 2.9.4, cssselect 1.2.0, parsel 1.8.1, w3lib 2.1.2, Twisted 22.10.0, Python 3.9.16 (main, Mar 16 2023, 14:22:29) - [Clang 14.0.0 (clang-1400.0.29.202)], pyOpenSSL 23.3.0 (OpenSSL 3.1.4 24 Oct 2023), cryptography 41.0.5, Platform macOS-12.6.5-arm64-arm-64bit
2023-10-29 21:49:57 [scrapy.addons] INFO: Enabled addons:
[]
2023-10-29 21:49:57 [asyncio] DEBUG: Using selector: KqueueSelector
2023-10-29 21:49:57 [scrapy.utils.log] DEBUG: Using reactor: twisted.internet.asyncioreactor.AsyncioSelectorReactor
2023-10-29 21:49:57 [scrapy.utils.log] DEBUG: Using asyncio event loop: asyncio.unix_events._UnixSelectorEventLoop
2023-10-29 21:49:57 [scrapy.extensions.telnet] INFO: Telnet Password: f1aab41d912ec7ff
2023-10-29 21:49:57 [scrapy.middleware] INFO: Enabled extensions:
['scrapy.extensions.corestats.CoreStats',
 'scrapy.extensions.telnet.TelnetConsole',
 'scrapy.extensions.memusage.MemoryUsage',
 'scrapy.extensions.logstats.LogStats']
2023-10-29 21:49:57 [scrapy.crawler] INFO: Overridden settings:
{'BOT_NAME': 'jsonrpc_crawler',
 'FEED_EXPORT_ENCODING': 'utf-8',
 'NEWSPIDER_MODULE': 'jsonrpc_crawler.spiders',
 'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
 'ROBOTSTXT_OBEY': True,
 'SPIDER_MODULES': ['jsonrpc_crawler.spiders'],
 'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
 'USER_AGENT': 'jsonrpc_crawler (+https://www.llamanodes.com)'}
2023-10-29 21:49:57 [scrapy.middleware] INFO: Enabled downloader middlewares:
['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
 'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
 'scrapy.downloadermiddlewares.retry.RetryMiddleware',
 'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
 'scrapy.downloadermiddlewares.stats.DownloaderStats']
2023-10-29 21:49:57 [scrapy.middleware] INFO: Enabled spider middlewares:
['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
 'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
 'scrapy.spidermiddlewares.referer.RefererMiddleware',
 'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
 'scrapy.spidermiddlewares.depth.DepthMiddleware']
2023-10-29 21:49:57 [scrapy.middleware] INFO: Enabled item pipelines:
[]
2023-10-29 21:49:57 [scrapy.core.engine] INFO: Spider opened
2023-10-29 21:49:57 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
2023-10-29 21:49:57 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023
2023-10-29 21:49:57 [scrapy-playwright] INFO: Starting download handler
2023-10-29 21:49:57 [scrapy-playwright] INFO: Starting download handler
2023-10-29 21:50:02 [scrapy.dupefilters] DEBUG: Filtered duplicate request: <GET https://curve.fi/#/ethereum/pools/3pool/deposit> - no more duplicates will be shown (see DUPEFILTER_DEBUG to show all duplicates)
2023-10-29 21:50:02 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://www.convexfinance.com/robots.txt> (referer: None)
2023-10-29 21:50:02 [protego] DEBUG: Rule at line 1 without any user agent to enforce it on.
2023-10-29 21:50:02 [scrapy-playwright] INFO: Launching browser chromium
2023-10-29 21:50:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://classic.curve.fi/robots.txt> (referer: None)
2023-10-29 21:50:02 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://curve.fi/robots.txt> (referer: None)
2023-10-29 21:50:02 [protego] DEBUG: Rule at line 7 without any user agent to enforce it on.
2023-10-29 21:50:02 [protego] DEBUG: Rule at line 11 without any user agent to enforce it on.
2023-10-29 21:50:02 [scrapy-playwright] INFO: Browser chromium launched
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: Browser context started: 'default' (persistent=False, remote=False)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] New page created, page count is 1 (1 for all contexts)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] New page created, page count is 2 (2 for all contexts)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] New page created, page count is 3 (3 for all contexts)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] Request: <GET https://www.convexfinance.com/> (resource type: document)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] Request: <GET https://curve.fi/> (resource type: document)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] Request: <GET https://classic.curve.fi/> (resource type: document)
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] Response: <200 https://classic.curve.fi/>
2023-10-29 21:50:02 [scrapy-playwright] DEBUG: [Context=default] Response: <200 https://www.convexfinance.com/>

...

2023-10-29 21:51:10 [scrapy.core.scraper] ERROR: Error downloading <GET https://curve.fi/>
Traceback (most recent call last):
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/twisted/internet/defer.py", line 1693, in _inlineCallbacks
    result = context.run(
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/twisted/python/failure.py", line 518, in throwExceptionIntoGenerator
    return g.throw(self.type, self.value, self.tb)
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/scrapy/core/downloader/middleware.py", line 54, in process_request
    return (yield download_func(request=request, spider=spider))
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/twisted/internet/defer.py", line 1065, in adapt
    extracted = result.result()
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/scrapy_playwright/handler.py", line 324, in _download_request
    return await self._download_request_with_page(request, page, spider)
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/scrapy_playwright/handler.py", line 372, in _download_request_with_page
    await self._apply_page_methods(page, request, spider)
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/scrapy_playwright/handler.py", line 485, in _apply_page_methods
    pm.result = await _maybe_await(method(*pm.args, **pm.kwargs))
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/scrapy_playwright/_utils.py", line 16, in _maybe_await
    return await obj
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/playwright/async_api/_generated.py", line 9358, in wait_for_load_state
    await self._impl_obj.wait_for_load_state(state=state, timeout=timeout)
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/playwright/_impl/_page.py", line 489, in wait_for_load_state
    return await self._main_frame.wait_for_load_state(**locals_to_params(locals()))
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/playwright/_impl/_frame.py", line 236, in wait_for_load_state
    return await self._wait_for_load_state_impl(state, timeout)
  File "/Users/bryan/.pyenv/versions/3.9.16/lib/python3.9/site-packages/playwright/_impl/_frame.py", line 264, in _wait_for_load_state_impl
    await wait_helper.result()
playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.

...

```

Then it sits and waits for all the rpcs to finish responding. You will have to wait for the slowest rpc, so you might want to skip some of the weaker free rpcs. Eventually it will print out something like this:

```
Endpoints:

0. "https://ethereum.llamarpc.com"

   Requests:   12.42 per second
   Timing:     0.0805s avg, 0.0589s min, 0.9229s max
               0.0799s standard deviation

   Percentiles:
     25% in 0.0623s
     50% in 0.0640s
     75% in 0.0712s
     90% in 0.0804s
     95% in 0.1223s
     99% in 0.6541s

   Errors: 0.00%

1. "https://rpc.ankr.com/eth"

   Requests:   12.88 per second
   Timing:     0.0776s avg, 0.0413s min, 0.3669s max
               0.0304s standard deviation

   Percentiles:
     25% in 0.0627s
     50% in 0.0722s
     75% in 0.0834s
     90% in 0.1035s
     95% in 0.1365s
     99% in 0.2317s

   Errors: 0.00%

2. "https://eth.drpc.org"

   Requests:   3.60 per second
   Timing:     0.2774s avg, 0.0593s min, 2.7413s max
               0.3903s standard deviation

   Percentiles:
     25% in 0.1773s
     50% in 0.1863s
     75% in 0.2309s
     90% in 0.4044s
     95% in 0.8604s
     99% in 2.3871s

   Errors: 0.00%

3. "https://eth.merkle.io"

   Requests:   9.83 per second
   Timing:     0.1017s avg, 0.0704s min, 3.0319s max
               0.1615s standard deviation

   Percentiles:
     25% in 0.0842s
     50% in 0.0917s
     75% in 0.0942s
     90% in 0.0969s
     95% in 0.1249s
     99% in 0.3248s

   Errors: 0.00%

4. "https://eth.meowrpc.com"

   Requests:   4.52 per second
   Timing:     0.2212s avg, 0.1853s min, 1.2732s max
               0.1066s standard deviation

   Percentiles:
     25% in 0.1905s
     50% in 0.1979s
     75% in 0.2033s
     90% in 0.2439s
     95% in 0.3548s
     99% in 0.7289s

   Errors: 0.00%

5. "https://1rpc.io/eth"

   Requests:   5.05 per second
   Timing:     0.1980s avg, 0.0408s min, 1.4986s max
               0.1080s standard deviation

   Percentiles:
     25% in 0.1674s
     50% in 0.1866s
     75% in 0.2092s
     90% in 0.2312s
     95% in 0.2632s
     99% in 0.6368s

   Errors: 0.00%

** Summary for 6 endpoints:
   Completed:  344 results with 2064 total requests
   Timing:     159.406237ms request avg, 1m53.6277915s total run time
   Errors:     0 (0.00%)
```

## Todo

- [ ] inject a provider at `window.ethereum`. Partially complete but needs more work. There's got to be a library for this already.
- [ ] after the page loads, click "connect wallet" buttons (if any). this usually starts a lot more requests
- [ ] helper script that replaces "latest" with a several block heights (archive number, recent number, latest as a number, and latest (the string)). then print all of the variants to stdout
- [ ] versus complains about "mismatches" on things like slightly different error messages. allow those
- [ ] finish webcrawler mode. it currently can scan for "a" links, but a lot of dapps don't use actual links. need to figure out how to find all the "clickable" things and what urls they will route to
