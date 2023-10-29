alert("This runs first");

// Set up a stub for window.ethereum
// This is designed to look like [MetaMask](https://docs.metamask.io/wallet/reference/provider-api/).
window.ethereum = {
    request: async function ({ method, params }) {
        if (method === 'eth_accounts') {
            return ['0x9eb9e3dc2543dc9FF4058e2A2DA43A855403F1fD'];
        }
        if (method === 'eth_sendTransaction') {
            // TODO: what should this return?
            return [];
        }
        // TODO: pass all the other methods to an actual provider
        return [];
    },
    isConnected: function () {
        return true;
    },
    isMetaMask: function () {
        // TODO: lie?
        return false;
    },
    isUnlocked: function () {
        return true;
    }
    // TODO: "on"
};
