from c1_fund_me.scripts.utils import get_account
from brownie import FundMe
import logging

logging.basicConfig(level='INFO')


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
    pass
