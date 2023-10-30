/* jsonrpc_crawler
 *
 */
console.log("llamanodes/jsonrpc_crawler start");

// TODO: random addresses are nice because they will be cache misses, but the accounts will always be empty
// satoshiandkin.eth has funds so the dapps will have actual values to work with
// TODO: more accounts. do some random maybe?
const ski_address = "0x9eb9e3dc2543dc9FF4058e2A2DA43A855403F1fD"

async function loadEthers() {
    if (typeof ethers === 'undefined') {
        console.log("injecting ethers");
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/ethers/6.8.0/ethers.umd.min.js';
        script.async = true;

        const loadPromise = new Promise((resolve, reject) => {
            script.onload = resolve;
            script.onerror = () => reject(new Error('Failed to load ethers library'));
        });

        document.head.appendChild(script);
        await loadPromise;
        console.log("ethers exists");
    } else {
        console.log("ethers already exists");
    }
}

// cache the provider so we don't have to get it every time
let _ethersProvider = null;

async function getEthersProvider() {
    if (!_ethersProvider) {
        await loadEthers();
        // TODO: use llamanodes? read config somehow?
        _ethersProvider = ethers.getDefaultProvider();
    }
    return _ethersProvider;
}

async function main() {
    // stub provider that accepts connections automatically
    const Eip1193Provider = {
        request: async function ({ method, params = [] }) {
            if (method === 'eth_accounts') {
                return [ski_address];
            }
            if (method === 'eth_sendTransaction') {
                return {
                    jsonrpc: "2.0",
                    error: {
                        code: -32601,
                        message: "eth_sendTransaction method is not supported"
                    },
                    id: null
                };
            }

            let provider = await getEthersProvider();

            // TODO: pass all the other methods to an actual provider
            return await provider.request(method, params);
        },
        isConnected: function () {
            return true;
        },
        isMetaMask: function () {
            // lie? i think we need "on" implemented
            return false;
        },
        isUnlocked: function () {
            return true;
        },
        // TODO: i think this isn't 
        on: async function (eventName, callback) {
            if (eventName === "connect") {
                callback({ "chainId": "0x1" })
            }
            if (eventName === "accountsChanged") {
                callback([ski_address]);
            }
        }
    };

    window.ethereum = Eip1193Provider;
}

main().then(() => {
    console.log("llamanodes/jsonrpc_crawler end");
});
