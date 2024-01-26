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
except ModuleNotFoundError:
    from schemas.mev_block import MevBlock
    from classifiers.event import EventLogClassifier
    from swaps import get_swaps
    from sandwiches import get_sandwiches
    from test_utils import load_test_sandwiches, TEST_SANDWICHES_DIRECTORY
    from agent import MEVBot
    from block_builder import get_block_builder


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
