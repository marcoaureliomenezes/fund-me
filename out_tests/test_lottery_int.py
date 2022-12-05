from c1_fund_me.scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_lottery
from brownie import network, exceptions, Lottery
from web3 import Web3
import pytest


def test_integration_get_entrance_fee():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    lottery = Lottery[-1]
    price = Web3.fromWei(lottery.getPrice(), "ether")
    entrance_fee = Web3.fromWei(lottery.getEntranceFee(), "ether")
    assert int(round(price * entrance_fee)) == 1000


def test_integration_can_run_lottery():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    lottery = Lottery[-1]
    print(lottery.lottery_state())
    owner_lottery, gambler1 = (get_account(), get_account(id="kandao-account"))
    tx_start = lottery.startLottery({"from": owner_lottery})
    tx_start.wait(1)
    tx_enter = lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    tx_enter.wait(1)
    assert lottery.players(0) == gambler1
    tx_end = lottery.endLottery({"from": owner_lottery})
    tx_end.wait(1)
    assert gambler1 == lottery.recentWinner()


def test_integration_can_end_lottery():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    lottery = Lottery[-1]
    owner_lottery, gambler1 = (Lottery.owner_lottery(), get_account(id="kandao-account"))
    lottery.startLottery({"from": owner_lottery})
    lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    lottery.endLottery({"from": owner_lottery})
    assert lottery.lottery_state() == 1

def test_integration_only_owner_can_end_lottery():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    lottery = Lottery[-1]
    owner_lottery, gambler1 = (Lottery.owner_lottery(), get_account(id="kandao-account"))
    lottery.startLottery({"from": owner_lottery})
    lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.endLottery({"from": gambler1})

def test_integration_prize_value():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for test networks")
    gamblers = ["digarupa-account", "kandao-account", "menopausa-account", "zeppelin-account"]
    owner = get_account()
    gambler1, gambler2, gambler3, gambler4 = [get_account(id=i) for i in gamblers]
    def check_balances():
        print(f"contract: {Web3.fromWei(lottery.balance(), 'ether')}"),
        print(f"Owner: {Web3.fromWei(owner.balance(), 'ether')}")
        print(f"Balances gamblers:\n\t {Web3.fromWei(gambler1.balance(), 'ether')}", 
                                        Web3.fromWei(gambler2.balance(), 'ether'))

    lottery = deploy_lottery(owner, 2000)
    lottery.startLottery({"from": owner})
    check_balances()
    lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    lottery.enter({"from": gambler2, "value": lottery.getEntranceFee()})
    lottery.enter({"from": gambler3, "value": lottery.getEntranceFee()})
    lottery.enter({"from": gambler4, "value": lottery.getEntranceFee()})
    check_balances()

    end_tx = lottery.endLottery({"from": owner})
    end_tx.wait(1)
    check_balances()

# def test_integration_can_pick_winner_correctly():
#     # Arrange
#     if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         pytest.skip()
#     lottery = deploy_lottery()
#     account = get_account()
#     lottery.startLottery({"from": account})
#     lottery.enter({"from": account, "value": lottery.getEntranceFee()})
#     lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
#     lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
#     fund_with_link(lottery)
#     starting_balance_of_account = account.balance()
#     balance_of_lottery = lottery.balance()
#     transaction = lottery.endLottery({"from": account})
#     request_id = transaction.events["RequestedRandomness"]["requestId"]
#     STATIC_RNG = 777
#     get_contract("vrf_coordinator").callBackWithRandomness(
#         request_id, STATIC_RNG, lottery.address, {"from": account}
#     )
#     # 777 % 3 = 0
#     assert lottery.recentWinner() == account
#     assert lottery.balance() == 0
#     assert account.balance() == starting_balance_of_account + balance_of_lottery