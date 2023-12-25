import random
import utils
from modules.account import Account
from loguru import logger


class Deployer:
    def __init__(self, acc: Account, bytecode: str = "0x") -> None:
        self.acc = acc
        self.bytecode = bytecode

    async def make_deploy(
        self,
    ):
        await self.acc.deploy_contract(self.bytecode)

    @staticmethod
    async def deploy(private_key: str, network: dict, contract: dict):
        acc = Account(private_key=private_key, network=network)
        logger.info(f"FROM {acc.address}")
        logger.info(f"NETWORK {network.get('name')}")
        logger.info(f"Name deploy contract {contract.get('name')}")
        deployre = Deployer(acc=acc, bytecode=contract.get("bytecode"))
        await deployre.make_deploy()

    @staticmethod
    async def create_database(wallets: list[str], params: dict) -> list[dict]:
        database: list[dict] = list()
        for param in params:
            for wallet in wallets:
                for i in range(random.randint(*param.get("count"))):
                    deploy_contract = random.choice(param.get("contracts"))
                    database.append(
                        {
                            "network": param.get("network"),
                            "private_key": wallet,
                            "contract": deploy_contract,
                        }
                    )
        return database

    @staticmethod
    async def deploy_with_database(settings=None):
        wallets = await utils.files.read_file_lines("files/wallets.txt")
        database = await Deployer.create_database(
            wallets=wallets, params=settings.params
        )
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.info(f"WALLET {counter}")
            await Deployer.deploy(
                private_key=data.get("private_key"),
                network=data.get("network"),
                contract=data.get("contract"),
            )
            await utils.time.sleep_view(settings.SLEEP)
            counter += 1