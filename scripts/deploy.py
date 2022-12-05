from brownie import FundMe, config, network
from scripts.utils import get_account, get_V3Aggregator
import logging
from web3 import Web3

logging.basicConfig(level='INFO')


def deploy_fund_me(owner, minimum_fee_usd, **kwargs):
    is_verified = config["networks"][network.show_active()].get("verify")
    price_feed_address = get_V3Aggregator(owner, decimals=kwargs['decimals'], initial_value=kwargs['initial_value'])
    fund_me = FundMe.deploy(price_feed_address,  minimum_fee_usd, {'from': owner}, publish_source=is_verified)
    return fund_me


def main():
    OWNER = get_account()
    MIN_FEE_USD, DECIMALS, INIT_VALUE = (100, 18, 2000)
    to_wei = lambda amount: Web3.toWei(amount, 'ether')
    deploy_fund_me(OWNER, to_wei(MIN_FEE_USD), decimals=DECIMALS, initial_value=to_wei(INIT_VALUE))



