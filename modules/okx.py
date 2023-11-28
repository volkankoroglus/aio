import pprint
import random
import ccxt
import utils
from loguru import logger


class OKX:
    def __init__(
        self, apiKey: str, secret: str, password: str, proxy: str = None
    ) -> None:
        self.okx = ccxt.okx(
            {
                "apiKey": apiKey,
                "secret": secret,
                "password": password,
                "enableRateLimit": True,
                "proxy": proxy,
            }
        )

    async def _get_fee(self, currency: str = None, chain: str = None):
        try:
            if chain == "Avalanche C-Chain":
                chain = "Avalanche C"
            if chain == "Avalanche X-Chain":
                chain = "Avalanche X"
            return self.okx.fetch_currencies()[currency]["networks"][chain]["fee"]
        except:
            logger.error("don't get fee")
            return None

    async def withdraw(self, address: str, currency: str, chain: str, amount: float):
        try:
            await self.withdraw_from_subaccs()
            logger.info(f"start withdraw {amount} {currency}-{chain} to {address}")
            self.okx.withdraw(
                currency,
                amount,
                address,
                {
                    "ccy": currency,
                    "amt": f"{amount}",
                    "dest": 4,
                    "toAddr": address,
                    "fee": await self._get_fee(currency=currency, chain=chain),
                    "chain": f"{currency}-{chain}",
                    "pwd": "-",
                },
            )
            logger.success(f"Withdraw {amount} {currency}-{chain} to {address}"),
        except Exception as e:
            logger.error(e)

    async def withdraw_from_subaccs(self):
        subacc_list = self.okx.private_get_users_subaccount_list()
        for subacc_data in subacc_list["data"]:
            try:
                subacc_name = subacc_data["subAcct"]
                for currency_data in self.okx.private_get_asset_subaccount_balances(
                    params={"subAcct": subacc_name}
                )["data"]:
                    balance = currency_data["availBal"]
                    ccy = currency_data["ccy"]
                    try:
                        self.okx.private_post_asset_transfer(
                            params={
                                "type": 2,  # from subacc to main
                                "ccy": ccy,  # currency
                                "amt": balance,  # amount
                                "from": 6,  # funding acc
                                "to": 6,  # funding acc
                                "subAcct": subacc_name,  # subacc_name
                            }
                        )
                        logger.info(
                            f"from {subacc_name} to MAIN transfer {balance} {ccy}"
                        )
                    except Exception as error:
                        logger.error(error)
            except Exception as error:
                logger.error(error)

    @staticmethod
    async def create_database(wallets: list[str], settings: list[dict]) -> list[dict]:
        tasks: list[dict] = list()
        print(settings)
        for param in settings.params:
            for wallet in (
                wallets
                if param["wallets_file"] == ""
                else await utils.files.read_file_lines(param["wallets_file"])
            ):
                round_number = random.randint(*param["round"])
                amount = round(
                    random.uniform(*param["amount"]),
                    round_number,
                )
                tasks.append(
                    {
                        "address": wallet,
                        "network": param["network"],
                        "ccy": param["symbol"],
                        "amount": amount,
                    }
                )
        return tasks

    @staticmethod
    async def withdraw_use_database(settings):
        wallets = await utils.files.read_file_lines("files/wallets.txt")
        settings = settings
        database = await OKX.create_database(wallets=wallets, settings=settings)
        # pprint.pprint(database)
        random.shuffle(database)

        okx = OKX(
            apiKey=settings.KEYS.get("api_key"),
            secret=settings.KEYS.get("api_secret"),
            password=settings.KEYS.get("password"),
            proxy=settings.PROXY,
        )
        counter = 1
        for wallet in database:
            logger.info(f"OPERATION {counter}/{len(database)}")
            await okx.withdraw(
                address=wallet["address"],
                amount=wallet["amount"],
                chain=wallet["network"],
                currency=wallet["ccy"],
            )
            await utils.time.sleep_view(settings.SLEEP)
            counter += 1


# def create_file_csv(okx):
#     with open("files/okx.csv", "w") as file:
#         writer = csv.writer(file)
#         writer.writerow(("token", "network", "fee", "min", "max"))
#         for token, data in okx.fetch_currencies().items():
#             for network, date_network in data["networks"].items():
#                 if date_network["active"]:
#                     fee = date_network["fee"]
#                     min_output = date_network["limits"]["withdraw"]["min"]
#                     max_output = date_network["limits"]["withdraw"]["max"]
#                     if network == "Avalanche C":
#                         network = "Avalanche C-Chain"
#                     if network == "Avalanche X":
#                         network = "Avalanche X-Chain"
#                     writer.writerow((token, network, fee, min_output, max_output))
