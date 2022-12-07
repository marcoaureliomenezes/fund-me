from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_fund_me, deploy_fund_me_factory, deploy_fund_me_unit
from brownie import network, exceptions, interface
from web3 import Web3
import pytest, logging

logging.basicConfig(level='INFO')



ETH_USD_VALUE = 2000
ETH_USD_DECIMALS = 18
MIN_DONATION_USD = 100
MIN_DONATION_ETH = MIN_DONATION_USD / ETH_USD_VALUE
BELOW_MIN_DONATION_ETH = (MIN_DONATION_USD - 1) / ETH_USD_VALUE

@pytest.fixture
def fundme():
    if network.show_active() not in LOCAL_CHAIN_ENV: return
    """
        deploy_fund_me_for_test with:
            - minimum fee of $100 USD.
            - 18 decimals for the pricefeed oracle contract.
            - price for ETH/USD = $2000 USD.
    """
    OWNER = get_account(index=0)
    min_donation_usd = Web3.toWei(MIN_DONATION_USD, 'ether')
    starting_price_eth_usd = Web3.toWei(ETH_USD_VALUE, 'ether')
    return deploy_fund_me(OWNER, min_donation_usd, decimals=ETH_USD_DECIMALS, initial_value=starting_price_eth_usd)


@pytest.fixture
def fundme_factory():
    if network.show_active() not in LOCAL_CHAIN_ENV: return
    OWNER = get_account(index=0)
    return deploy_fund_me_factory(OWNER)



def test_is_deployer_the_owner(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER = get_account(index=0)
    assert fundme.owner() == OWNER.address


def test_variables_were_initialized_as_expected(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    assert ETH_USD_DECIMALS == fundme.getDecimals()
    assert MIN_DONATION_USD == Web3.fromWei(fundme.entranceFeeUSD(), 'ether')
    assert ETH_USD_VALUE == Web3.fromWei(fundme.getPrice(), 'ether')


def test_convert_eth_to_usd_is_working(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    price = fundme.getConversionRate(Web3.toWei(MIN_DONATION_ETH, 'ether'))
    assert Web3.fromWei(price, 'ether') == MIN_DONATION_ETH * ETH_USD_VALUE


def test_funder_has_not_resources_enough(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    FUNDER = get_account(index=1)
    with pytest.raises(exceptions.VirtualMachineError):
        tx = fundme.fund({"from": FUNDER, "value": Web3.toWei(BELOW_MIN_DONATION_ETH, 'ether')})


def test_funder_can_successfully_fund(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    FUNDER = get_account(index=1)
    tx = fundme.fund({"from": FUNDER, "value": Web3.toWei(MIN_DONATION_ETH, 'ether')})
    assert MIN_DONATION_ETH == float(Web3.fromWei(fundme.addressToAmountFunded(FUNDER), 'ether'))


def test_only_owner_can_withdraw(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    HACKER = get_account(index=7)
    FUNDER = get_account(index=1)
    tx = fundme.fund({"from": FUNDER, "value": Web3.toWei(MIN_DONATION_ETH, 'ether')})
    with pytest.raises(exceptions.VirtualMachineError):
        tx = fundme.withDraw({"from": FUNDER})
    with pytest.raises(exceptions.VirtualMachineError):
        tx = fundme.withDraw({"from": HACKER})


def test_owner_withdraw_correctly(fundme):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER = get_account(index=0)
    FUNDER = get_account(index=1)
    BALANCE_OWNER_BEFORE = OWNER.balance()
    tx = fundme.fund({"from": FUNDER, "value": Web3.toWei(MIN_DONATION_ETH, 'ether')})
    tx = fundme.fund({"from": FUNDER, "value": Web3.toWei(MIN_DONATION_ETH, 'ether')})
    tx = fundme.withDraw({"from": OWNER})
    AMOUNT_WITHDRAWED = OWNER.balance() - BALANCE_OWNER_BEFORE
    assert MIN_DONATION_ETH * 2 == float(Web3.fromWei(AMOUNT_WITHDRAWED, 'ether'))




def test_is_factory_working(fundme_factory):
    if network.show_active() not in LOCAL_CHAIN_ENV: pytest.skip("only for local test")
    OWNER = get_account(index=0)
    fund_me = deploy_fund_me_unit(fundme_factory, OWNER, Web3.toWei(MIN_DONATION_USD, "ether"), decimals=ETH_USD_DECIMALS, initial_value=Web3.toWei(ETH_USD_VALUE, 'ether'))
    FUNDER = get_account(index=1)
    fund_me_contract = interface.IFundMe(fund_me)
    print("res")
    BALANCE_OWNER_BEFORE = OWNER.balance()
    tx = fund_me_contract.fund({"from": FUNDER, "value": Web3.toWei(MIN_DONATION_ETH, 'ether')})
    tx = fund_me_contract.fund({"from": FUNDER, "value": Web3.toWei(MIN_DONATION_ETH, 'ether')})
    tx = fund_me_contract.withDraw({"from": OWNER})
    AMOUNT_WITHDRAWED = OWNER.balance() - BALANCE_OWNER_BEFORE
    assert MIN_DONATION_ETH * 2 == float(Web3.fromWei(AMOUNT_WITHDRAWED, 'ether'))

