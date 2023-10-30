# jsonrpc_crawler
crawl dapps and extract all their jsonrpc requests

## Usage

In your terminal:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
scrapy crawl jsonrpc | versus https://ethereum.llamarpc.com https://ethereum-staging.llamarpc.com https://rpc.ankr.com/eth
```
