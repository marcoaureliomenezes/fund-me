from c1_fund_me.scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy_mocks import deploy_MockV3Aggregator
from brownie import network, exceptions, FundMe
from web3 import Web3
import pytest


def test_deploy():
    # if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     pytest.skip("only for local test")
    account_7 = get_account(index=7)
    previous_balance = account_7.balance()
    mock_v3 = deploy_MockV3Aggregator(account_7)
    expected_roundId, expected_answer, expected_answeredInRound = (1, 2000 * 10**8, 1)
    roundId, answer, startedAt, updatedAt, answeredInRound = mock_v3.latestRoundData()
    assert mock_v3.decimals() == 8
    assert mock_v3.description() == "v0.6/tests/MockV3Aggregator.sol"
    assert answer == expected_answer
    assert roundId == expected_roundId
    assert answeredInRound == expected_answeredInRound
