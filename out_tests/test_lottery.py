from c1_fund_me.scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy import deploy_lottery
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner = get_account(index=0)
    lottery = deploy_lottery(owner, 2000)
    expected_entrance_fee = Web3.toWei(1, "ether")
    entrance_fee = lottery.getEntranceFee()
    print(Web3.fromWei(lottery.getPrice(), "ether"))
    print(Web3.fromWei(entrance_fee, "ether"))
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner = get_account(index=0)
    lottery = deploy_lottery(owner, 2000)
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner, gambler1 = (get_account(index=0), get_account(index=1))
    lottery = deploy_lottery(owner, 2000)
    lottery.startLottery({"from": owner})
    lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == gambler1


def test_only_owner_can_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner, gambler1 = (get_account(index=0), get_account(index=1))
    lottery = deploy_lottery(owner, 2000)
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.startLottery({"from": gambler1})


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner, gambler1 = (get_account(index=0), get_account(index=1))
    lottery = deploy_lottery(owner, 2000)
    lottery.startLottery({"from": owner})
    lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    lottery.endLottery({"from": owner})
    assert lottery.lottery_state() == 1


def test_only_owner_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner, gambler1 = (get_account(index=0), get_account(index=1))
    lottery = deploy_lottery(owner, 2000)
    lottery.startLottery({"from": owner})
    lottery.enter({"from": gambler1, "value": lottery.getEntranceFee()})
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.endLottery({"from": gambler1})

def test_prize_value():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    owner, gambler1, gambler2 = [get_account(index=i) for i in range(3)]
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
    check_balances()

    end_tx = lottery.endLottery({"from": owner})
    end_tx.wait(1)
    check_balances()

# def test_can_pick_winner_correctly():
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