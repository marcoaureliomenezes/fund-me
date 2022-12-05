from scripts.utils import LOCAL_CHAIN_ENV, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, exceptions, FundMe
from web3 import Web3
import pytest


