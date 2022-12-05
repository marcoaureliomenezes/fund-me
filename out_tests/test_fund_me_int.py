from c1_fund_me.scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, exceptions, FundMe
from web3 import Web3
import pytest


def test_deploy():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    account_7 = get_account(index=7)
    fund_me = deploy_fund_me(account_7)
    assert fund_me.owner() == account_7.address

def test_get_version():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    FAKE_PRICE = 2000 * 10**18
    ENTRANCE_FEE = int((50 * 10**36) / FAKE_PRICE) + 1
    account_7 = get_account(index=7)
    fund_me = deploy_fund_me(account_7)
    assert fund_me.getVersion() == 1
    assert fund_me.getPrice() == FAKE_PRICE
    assert fund_me.getEntranceFee() == ENTRANCE_FEE


def test_simple_fund_and_withdraw():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    dadaia_account = get_account()
    kandao_account = get_account(id='kandao-account')
    fund_me = deploy_fund_me(dadaia_account)
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    tx = fund_me.fund({"from": kandao_account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(kandao_account.address) == entrance_fee
    tx2 = fund_me.withDraw({"from": dadaia_account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(kandao_account.address) == 0


# def test_fund():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         pytest.skip("only for local test")
#     fund_me = deploy_fund_me(index=7)
    
    
# def test_only_owner_can_withDraw():
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         pytest.skip("only for local test")
#     fund_me = deploy_fund_me(index=7)
#     bad_actor = deploy_fund_me(index=5)
#     fund_me.withDraw({"from": bad_actor})
#     with pytest.raises(exceptions.VirtualMachineError):
#         fund_me.withdraw({"from": bad_actor})