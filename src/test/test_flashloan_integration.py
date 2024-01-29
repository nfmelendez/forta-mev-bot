
import pickle

try:
    from src.schemas.mev_block import MevBlock
    from src.classifiers.event import EventLogClassifier
    from src.swaps import get_swaps
    from src.arbitrages import get_arbitrages
    from src.flashloans import get_flashloans
    from src.test_utils import TEST_ARBITRAGES_DIRECTORY
    from src.agent import MEVBot
    from src.block_builder import get_block_builder
except ModuleNotFoundError:
    from schemas.mev_block import MevBlock
    from classifiers.event import EventLogClassifier
    from swaps import get_swaps
    from arbitrages import get_arbitrages
    from test_utils import TEST_ARBITRAGES_DIRECTORY
    from agent import MEVBot
    from flashloans import get_flashloans
    from block_builder import get_block_builder


def test_makerdao_flashloan():
    target_transaction = "0xa396efdef0d1f0b6d636cd8340ef0d4bd5d00da16f354b49e149bfc66f2040cf"
    classifier = EventLogClassifier()
    pkl_file = open(f"{TEST_ARBITRAGES_DIRECTORY}/19111847-makerdao-flashloan.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    transactions = [t for t in block.transactions if t.hash == target_transaction]
    block.transactions = transactions
    classified_event = classifier.classify(block.transactions)

    flashloans = get_flashloans(classified_event)

    assert len(flashloans) == 1

    maker_flashloan = flashloans[0]

    assert maker_flashloan.asset == "0x6b175474e89094c44da98b954eedeac495271d0f"
    assert maker_flashloan.amount == 100000000000000000000000000



def test_balancer_flashloan():
    target_transaction = "0xf3f27bfffc4cf1e65206a3c98349f919d9ba4324da9f16a338106ee6d394879f"
    classifier = EventLogClassifier()
    pkl_file = open(f"{TEST_ARBITRAGES_DIRECTORY}/18413144-balancer-flahloan.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    transactions = [t for t in block.transactions if t.hash == target_transaction]
    block.transactions = transactions
    classified_event = classifier.classify(block.transactions)

    flashloans = get_flashloans(classified_event)

    assert len(flashloans) == 1

    maker_flashloan = flashloans[0]

    assert maker_flashloan.asset == "0x6b175474e89094c44da98b954eedeac495271d0f"
    assert maker_flashloan.amount == 590530332275705506693120



def test_dodo_flashloan():
    target_transaction = "0x0b062361e16a2ea0942cc1b4462b6584208c8c864609ff73aaa640aaa2d92428"
    classifier = EventLogClassifier()
    pkl_file = open(f"{TEST_ARBITRAGES_DIRECTORY}/12000102-dodo-flahloan.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    transactions = [t for t in block.transactions if t.hash == target_transaction]
    block.transactions = transactions
    classified_event = classifier.classify(block.transactions)

    flashloans = get_flashloans(classified_event)

    assert len(flashloans) == 1

    maker_flashloan = flashloans[0]

    assert maker_flashloan.asset == "0xdac17f958d2ee523a2206206994597c13d831ec7"
    assert maker_flashloan.amount == 326070162808
