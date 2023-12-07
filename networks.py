class Networks:
    ethereum = {
        "name": "ethereum",
        "rpc": [
            "https://eth.llamarpc.com",
            "wss://ethereum.publicnode.com",
            "https://rpc.mevblocker.io",
        ],
        "scan": "https://etherscan.io/",
        "eip1559": True,
        "token": "ETH",
    }

    arbitrum = {
        "name": "arbitrum",
        "rpc": [
            "https://arbitrum.llamarpc.com",
            "wss://arbitrum-one.publicnode.com",
            "https://endpoints.omniatech.io/v1/arbitrum/one/public",
        ],
        "scan": "https://arbiscan.io/",
        "eip1559": True,
        "token": "ETH",
    }

    optimism = {
        "name": "optimism",
        "rpc": [
            "https://optimism.llamarpc.com",
            "wss://optimism.publicnode.com",
            "https://mainnet.optimism.io",
        ],
        "scan": "https://optimistic.etherscan.io/",
        "eip1559": True,
        "token": "ETH",
    }

    base = {
        "name": "base",
        "rpc": ["https://base.llamarpc.com"],
        "scan": "https://basescan.org/",
        "eip1559": True,
        "token": "ETH",
    }

    avalanche = {
        "name": "avalanche",
        "rpc": [
            "https://avalanche.drpc.org",
            "https://api.avax.network/ext/bc/C/rpc",
            "https://1rpc.io/avax/c",
        ],
        "scan": "https://snowtrace.io/",
        "eip1559": True,
        "token": "AVAX",
    }

    polygon = {
        "name": "polygon",
        "rpc": [
            "https://polygon.llamarpc.com",
            "wss://polygon-bor.publicnode.com",
        ],
        "scan": "https://polygonscan.com/",
        "eip1559": True,
        "token": "MATIC",
    }

    scroll = {
        "name": "scroll",
        "rpc": [
            "https://scroll.blockpi.network/v1/rpc/public",
            "https://rpc-scroll.icecreamswap.com",
            "https://rpc.ankr.com/scroll",
        ],
        "scan": "https://scrollscan.com/",
        "eip1559": False,
        "token": "ETH",
    }

    linea = {
        "name": "linea",
        "rpc": [
            "https://linea.blockpi.network/v1/rpc/public",
            "https://rpc.linea.build",
        ],
        "scan": "https://lineascan.build/",
        "eip1559": False,
        "token": "ETH",
    }