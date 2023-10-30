# jsonrpc_crawler
crawl dapps and extract all their jsonrpc requests

## Usage

In your terminal:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
scrapy crawl jsonrpc | jq -c .request | versus https://ethereum.llamarpc.com https://rpc.ankr.com/eth https://eth.drpc.org https://eth.merkle.io https://eth.meowrpc.com https://1rpc.io/eth
```

Example output starts with a bunch of debug logs that don't matter so much.

```
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
