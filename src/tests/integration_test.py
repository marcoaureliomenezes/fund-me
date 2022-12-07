from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, exceptions, FundMe
from web3 import Web3
import pytest


# def deploy_for_test(OWNER):
#     MIN_FEE_USD, DECIMALS, INIT_VALUE = (100, 18, 2000)
#     return deploy_fund_me(OWNER, Web3.toWei(MIN_FEE_USD, 'ether'), decimals=DECIMALS, initial_value=Web3.toWei(INIT_VALUE, 'ether'))



# def test_only_owner_can_withdraw():
#     OWNER = get_account(id="dadaia")
#     FUNDER1 = get_account(id="kandao")
#     FUNDER2 = get_account(id="maiquinhas")
#     DONATE_BY_FUNDER1, DONATE_BY_FUNDER2 = (0.1, 0.1)
#     fund_me = deploy_for_test(OWNER)
#     _ = fund_me.fund({"from": FUNDER1, "value": Web3.toWei(DONATE_BY_FUNDER1, 'ether')})
#     _ = fund_me.fund({"from": FUNDER2, "value": Web3.toWei(DONATE_BY_FUNDER2, 'ether')})
#     with pytest.raises(exceptions.VirtualMachineError):
#         _ = fund_me.withDraw({"from": FUNDER1})
#     BALANCE_OWNER_BEFORE = OWNER.balance()
#     _ = fund_me.withDraw({"from": OWNER})
#     WITHDRAWED = OWNER.balance() - BALANCE_OWNER_BEFORE
#     assert DONATE_BY_FUNDER1 + DONATE_BY_FUNDER2 == float(Web3.fromWei(WITHDRAWED, 'ether'))