from brownie import network, accounts, config, MockV3Aggregator, Contract
import logging

NON_FORKED_LOCAL_CHAIN = ["development", "ganache-dadaia"]
FORKED_LOCAL_CHAIN = ["mainnet-fork"]
LOCAL_CHAIN_ENV = NON_FORKED_LOCAL_CHAIN + FORKED_LOCAL_CHAIN


def get_account(**kwargs):
    is_local = network.show_active() in LOCAL_CHAIN_ENV
    if is_local and kwargs.get('index'): return accounts[kwargs["index"]]
    elif is_local and not kwargs.get('index'): return accounts[0]
    elif not is_local and kwargs.get("id"): return accounts.load(kwargs["id"])
    else: return accounts.add(config["wallets"]["from_key"])



def deploy_MockV3Aggregator(owner, decimals, initial_value):
    logging.info("Deploying new MockV3Aggregator...")
    price_feed_contract = MockV3Aggregator.deploy(decimals, initial_value, {"from": owner})
    logging.info("New MockV3Aggregator Deployed!")
    return price_feed_contract

def get_V3Aggregator(owner, decimals=18, initial_value=0):
    chain = network.show_active()
    if chain not in LOCAL_CHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
        logging.info(f"V3Aggregator address on {chain} network deployed at {price_feed_address}")
        return price_feed_address
    elif len(MockV3Aggregator) == 0:
        new_mock_v3_aggregator = deploy_MockV3Aggregator(owner, decimals, initial_value)
        return new_mock_v3_aggregator.address
    else:
        latest_mock_v3_aggregator = MockV3Aggregator[-1].address
        logging.info(f"MockV3Aggregator address already deployed on address {latest_mock_v3_aggregator}")
        return latest_mock_v3_aggregator


# def get_publish_source():
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or not os.getenv("ETHERSCAN_TOKEN"):
#         return False
#     return True


# def get_breed(breed_number):
#     switch = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
#     return switch[breed_number]




# def get_verify_status():
#     verify = config["networks"][network.show_active()].get("verify")
#     return verify if verify else False

# #############################    DEPLOYING MOCKS    ####################################


# def listen_for_event(brownie_contract, event, timeout=200, poll_interval=2):
#     """Listen for an event to be fired from a contract.
#     We are waiting for the event to return, so this function is blocking.

#     Args:
#         brownie_contract ([brownie.network.contract.ProjectContract]):
#         A brownie contract of some kind.

#         event ([string]): The event you'd like to listen for.

#         timeout (int, optional): The max amount in seconds you'd like to
#         wait for that event to fire. Defaults to 200 seconds.

#         poll_interval ([int]): How often to call your node to check for events.
#         Defaults to 2 seconds.
#     """
#     web3_contract = web3.eth.contract(
#         address=brownie_contract.address, abi=brownie_contract.abi
#     )
#     start_time = time.time()
#     current_time = time.time()
#     event_filter = web3_contract.events[event].createFilter(fromBlock="latest")
#     while current_time - start_time < timeout:
#         for event_response in event_filter.get_new_entries():
#             if event in event_response.event:
#                 print("Found event!")
#                 return event_response
#         time.sleep(poll_interval)
#         current_time = time.time()
#     print("Timeout reached, no event found.")
#     return {"event": None}