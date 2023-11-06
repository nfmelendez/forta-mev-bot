from typing import List
import pickle


try:
    from src.schemas.mev_block import MevBlock
    from src.classifiers.event import EventLogClassifier
    from src.test_utils import TEST_LIQUIDATION_DIRECTORY
    from src.agent import MEVBot
    from src.schemas.events import Protocol
    from src.schemas.prices import ETH_TOKEN_ADDRESS
    from src.schemas.liquidations import Liquidation
    from src.liquidations import get_liquidations

except ModuleNotFoundError:
    from schemas.mev_block import MevBlock
    from classifiers.event import EventLogClassifier
    from test_utils import TEST_LIQUIDATION_DIRECTORY
    from agent import MEVBot
    from schemas.events import Protocol
    from schemas.prices import ETH_TOKEN_ADDRESS
    from schemas.liquidations import Liquidation
    from liquidations import get_liquidations

def test_single_weth_liquidation():
    transaction_hash = (
        "0xb7575eedc9d8cfe82c4a11cd1a851221f2eafb93d738301995ac7103ffe877f7"
    )
    block_number = 13244807

    liquidations = [
        Liquidation(
            liquidated_user="0xd16404ca0a74a15e66d8ad7c925592fb02422ffe",
            liquidator_user="0x19256c009781bc2d1545db745af6dfd30c7e9cfa",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=26503300291,
            received_amount=8182733924513576561,
            received_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            log_index=29,
            block_number=block_number,
            error=None,
            receive_a_token=False,
            bot_owner='0x033f20cff835ef32243c13bae0ff283afddaaf25'
        )
    ]

    pkl_file = open(f"{TEST_LIQUIDATION_DIRECTORY}/{block_number}.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    classifier = EventLogClassifier()
    classified_transactions = classifier.classify(block.transactions)
    result = get_liquidations(classified_transactions)

    for liquidation in liquidations:
        assert liquidation in result



def test_single_liquidation_with_atoken_payback():
    transaction_hash = (
        "0xde551a73e813f1a1e5c843ac2c6a0e40d71618f4040bb7d0cd7cf7b2b6cf4633"
    )
    block_number = 13376024

    liquidations = [
        Liquidation(
            liquidated_user="0x3d2b6eacd1bca51af57ed8b3ff9ef0bd8ee8c56d",
            liquidator_user="0x887668f2dc9612280243f2a6ef834cecf456654e",
            debt_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            debt_purchase_amount=767615458043667978,
            received_amount=113993647930952952550,
            received_token_address="0xa06bc25b5805d5f8d82847d191cb4af5a3e873e0",
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            log_index=89,
            block_number=block_number,
            error=None,
            receive_a_token=True,
            bot_owner='0x1f564b813b6f51f705b9b392d0d3388602fb3848'
        )
    ]

    pkl_file = open(f"{TEST_LIQUIDATION_DIRECTORY}/{block_number}.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    classifier = EventLogClassifier()

    classified_events = classifier.classify(block.transactions)
    result = get_liquidations(classified_events)

    for liquidation in liquidations:
        assert liquidation in result



def _assert_equal_list_of_liquidations(
    actual_liquidations: List[Liquidation], expected_liquidations: List[Liquidation]
):
    for i in range(len(actual_liquidations)):
        assert actual_liquidations[i] == expected_liquidations[i]
