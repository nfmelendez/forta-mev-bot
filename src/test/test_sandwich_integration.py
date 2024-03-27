from unittest.mock import Mock
import pickle
try:
    from src.schemas.mev_block import MevBlock
    from src.classifiers.event import EventLogClassifier
    from src.swaps import get_swaps
    from src.sandwiches import get_sandwiches
    from src.test_utils import load_test_sandwiches, TEST_SANDWICHES_DIRECTORY
    from src.agent import MEVBot
    from src.block_builder import get_block_builder
    from src.arbitrages import get_arbitrages
    from src.flashloans import get_flashloans
except ModuleNotFoundError:
    from schemas.mev_block import MevBlock
    from classifiers.event import EventLogClassifier
    from swaps import get_swaps
    from sandwiches import get_sandwiches
    from test_utils import load_test_sandwiches, TEST_SANDWICHES_DIRECTORY
    from agent import MEVBot
    from block_builder import get_block_builder
    from arbitrages import get_arbitrages
    from flashloans import get_flashloans


class TestMEVBot:

    def test_sandwitch(self):
        pkl_file = open(f"{TEST_SANDWICHES_DIRECTORY}/12775690.pkl", 'rb')
        expected_sandwiches = load_test_sandwiches(12775690)

        block: MevBlock = pickle.load(pkl_file)
        classifier = EventLogClassifier()
        classified_events = classifier.classify(block.transactions)
        swaps = get_swaps(classified_events)
        assert len(swaps) == 22
        block_builder = get_block_builder(block.block.block.miner, block.block.network)
        sandwiches = get_sandwiches(block.block.network, list(swaps))
        assert sandwiches == expected_sandwiches


    def test_sandwitch_router_should_not_create_alarm(self):
        banana_gun_router = "0x3328f7f4a1d1c57c35df56bbf0c9dcafca309c49"
        pkl_file = open(f"{TEST_SANDWICHES_DIRECTORY}/18791504-router-sandwich.pkl", 'rb')

        block: MevBlock = pickle.load(pkl_file)
        classifier = EventLogClassifier()
        classified_events = classifier.classify(block.transactions)
        swaps = get_swaps(classified_events)
        sandwiches = get_sandwiches(block.block.network, list(swaps))
        assert len(sandwiches) == 2


    def test_sandwitch_for_double_victims_and_arb_backrun_thx(self):
        mev_bot = MEVBot()
        pkl_file = open(f"{TEST_SANDWICHES_DIRECTORY}/19270423-double-victim-sandwich.pkl", 'rb')
        block: MevBlock = pickle.load(pkl_file)
        classifier = EventLogClassifier()
        classified_events = classifier.classify(block.transactions)
        swaps = get_swaps(classified_events)
        sandwiches = get_sandwiches(block.block.network, list(swaps))
        assert len(sandwiches) == 2
        flashloans = get_flashloans(classified_events)
        block_builder = get_block_builder(block.block.block.miner, block.block.network)

        arbitrages = get_arbitrages(list(swaps), flashloans)
        sandwich_findings = mev_bot.create_sandwich_finding(sandwiches, None)
        assert len(sandwich_findings) == 1
        sandwich_findings[0].metadata['evidence.list_sandwich_transactions'] == '0x53342ef914ad938ee6e3f45fa84e9c3a9dfae16a5368bf5665791ab2d5849d11, 0xa40de807fcc0fcec70b37c548c63c24e26b425e25631eb94d990a549242cb3c9'
        arb_findings = mev_bot.create_arbitrage_finding(arbitrages, None)
        assert len(arb_findings) == 1

