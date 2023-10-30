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

## Todo

- [ ] inject a provider at `window.ethereum`. Partially complete but needs more work. There's got to be a library for this already.
- [ ] click "connect wallet" buttons (if any). this usually starts a lot more requests
- [ ] helper script that replaces "latest" with a several block heights (archive number, recent number, latest as a number, and latest (the string)). then print all of the variants to stdout
- [ ] versus complains about "mismatches" on things like slightly different error messages. allow those
