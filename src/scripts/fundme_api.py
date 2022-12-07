from scripts.utils import get_account, get_V3Aggregator
from brownie import FundMe, FundMeFactory
from scripts.deploy import deploy_fund_me_Factory
from web3 import Web3
import logging

logging.basicConfig(level='INFO')



def create_fundMe():
    FundMeFactory

def fund_contract():
    funder =  get_account(index=7)
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee()
    logging.info(f"Current entry fee is {entrance_fee}. Funding...")
    fund_me.fund({"from": funder, "value": entrance_fee * 500})


def withdraw_contract():
    owner =  get_account()
    fund_me = FundMe[-1]
    fund_me.withDraw({"from": owner})




def main():
    owner = get_account()
    
    fund_factory = deploy_fund_me_Factory(owner)
    MIN_FEE_USD, DECIMALS, INIT_VALUE = (100, 18, 2000)
    to_wei = lambda amount: Web3.toWei(amount, 'ether')
    price_feed_address = get_V3Aggregator(owner, decimals=DECIMALS, initial_value=to_wei(INIT_VALUE))
    address = fund_factory.createFundMeContract(price_feed_address, to_wei(MIN_FEE_USD), {'from': owner})
    print(f"O ADDRESS AQUI {address}")

