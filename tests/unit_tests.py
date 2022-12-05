from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, exceptions
from web3 import Web3
import pytest


def test_deploy():
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER, HACKER = (get_account(index=0), get_account(index=1))
    MIN_FEE_USD, DECIMALS, INIT_VALUE = (100, 18, 2000)
    fund_me = deploy_fund_me(OWNER, Web3.toWei(MIN_FEE_USD, 'ether'), decimals=DECIMALS, initial_value=Web3.toWei(INIT_VALUE, 'ether'))
    assert fund_me.owner() == OWNER.address
    assert fund_me.owner() != HACKER.address
    assert DECIMALS == fund_me.getDecimals()
    assert MIN_FEE_USD == Web3.fromWei(fund_me.entranceFeeUSD(), 'ether')
    

def deploy_for_test(OWNER):
    MIN_FEE_USD, DECIMALS, INIT_VALUE = (100, 18, 2000)
    return deploy_fund_me(OWNER, Web3.toWei(MIN_FEE_USD, 'ether'), decimals=DECIMALS, initial_value=Web3.toWei(INIT_VALUE, 'ether'))


def test_get_price():
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER, INIT_VALUE = (get_account(), 2000)
    fund_me = deploy_for_test(OWNER)
    price = fund_me.getPrice()
    assert INIT_VALUE == Web3.fromWei(price, 'ether')


def test_get_conversion_rate():
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER, AMOUNT_IN, INIT_VALUE = (get_account(), 0.25, 2000)
    fund_me = deploy_for_test(OWNER)
    price = fund_me.getConversionRate(Web3.toWei(AMOUNT_IN, 'ether'))
    assert Web3.fromWei(price, 'ether') == AMOUNT_IN * INIT_VALUE


def test_get_entrance():
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER, AMOUNT_IN, INIT_VALUE = (get_account(), 0.05, 2000)
    AMOUNT_IN_WEI = Web3.toWei(AMOUNT_IN, 'ether')
    fund_me = deploy_for_test(OWNER)
    entrance = fund_me.convertEntranceFee(AMOUNT_IN_WEI)
    print(Web3.fromWei(entrance, 'ether'))
    assert AMOUNT_IN * INIT_VALUE == Web3.fromWei(entrance, 'ether')


def test_fund_me():
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER, FUNDER, INIT_VALUE = (get_account(index=0), get_account(index=1), 2000)
    fund_me = deploy_for_test(OWNER)
    BELOW_REQUIRED, ABOVE_REQUIRED = ((100 - 1) / INIT_VALUE, 100 / INIT_VALUE)
    with pytest.raises(exceptions.VirtualMachineError):
        _ = fund_me.fund({"from": FUNDER, "value": Web3.toWei(BELOW_REQUIRED, 'ether')})
    _ = fund_me.fund({"from": FUNDER, "value": Web3.toWei(ABOVE_REQUIRED, 'ether')})
    assert ABOVE_REQUIRED == float(Web3.fromWei(fund_me.addressToAmountFunded(FUNDER), 'ether'))



def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER, FUNDER1, FUNDER2= (get_account(index=0), get_account(index=1), get_account(index=2))
    DONATE_BY_FUNDER1, DONATE_BY_FUNDER2 = (0.1, 0.1)
    fund_me = deploy_for_test(OWNER)
    _ = fund_me.fund({"from": FUNDER1, "value": Web3.toWei(DONATE_BY_FUNDER1, 'ether')})
    _ = fund_me.fund({"from": FUNDER2, "value": Web3.toWei(DONATE_BY_FUNDER2, 'ether')})
    with pytest.raises(exceptions.VirtualMachineError):
        _ = fund_me.withDraw({"from": FUNDER1})
    BALANCE_OWNER_BEFORE = OWNER.balance()
    _ = fund_me.withDraw({"from": OWNER})
    WITHDRAWED = OWNER.balance() - BALANCE_OWNER_BEFORE
    assert DONATE_BY_FUNDER1 + DONATE_BY_FUNDER2 == float(Web3.fromWei(WITHDRAWED, 'ether'))

