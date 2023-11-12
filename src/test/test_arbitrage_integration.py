
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

reverted_transactions_of_12914944 = ["0x060918d6c60e45fd4ade3af33e911ba8fae26a7dce2a9f445198317c5edf51a9","0x0a0cdc10390f60a27837ca278c9cd718a00a5dfa88982359c03eeb48507a5d8f","0x0a0cdc10390f60a27837ca278c9cd718a00a5dfa88982359c03eeb48507a5d8f","0x21e95dfe2ea08aabf95bab653a5ed462a2a05b2693beef3d53edcf0407e867f9","0x24220dd35e275fb59acd65c34b947f40cce9dc60b8cabba59138f40b1f876792","0x24220dd35e275fb59acd65c34b947f40cce9dc60b8cabba59138f40b1f876792","0x2aab262669b0b0ca9c5d5e5dc9e39c34b0f541934e4282705913342b8be0b834","0x332ac6d600678efd2d69defdabd166704e427c6ec2c8cf40ddcfdcc739476754","0x378be0df4410ee829e732b105f20e9eb64f6d512fba92770f150a30763fd39c5","0x378be0df4410ee829e732b105f20e9eb64f6d512fba92770f150a30763fd39c5","0x448245bf1a507b73516c4eeee01611927dada6610bf26d403012f2e66800d8f0","0x448245bf1a507b73516c4eeee01611927dada6610bf26d403012f2e66800d8f0","0x448245bf1a507b73516c4eeee01611927dada6610bf26d403012f2e66800d8f0","0x473f1e61827f40bf488f7652f79e14f493eeafd0c561d2c16cfa5976faeec4f1","0x473f1e61827f40bf488f7652f79e14f493eeafd0c561d2c16cfa5976faeec4f1","0x4d77bd740fd35d40ac1baf62f9d53e36ca434ba1064645577e147ce26ad6c3d0","0x528ef48a6d988189d49b0f2bbd62f18cadacae23e49f7ba0da3256661841519c","0x5aed0bd57f54d35bc16ce70632620eefdb1fcd772b99250cad9a71fb91901e58","0x5aed0bd57f54d35bc16ce70632620eefdb1fcd772b99250cad9a71fb91901e58","0x614ab1996606f7818c2c11f6c182fe61036c70eba0a83f8af6134240b702f525","0x71f6ee490810e448267f27136eb29c5ccafb590fc293f1bc483668a3610601dc","0x73dd2e4bd4fcb71a7e96c2ff3f32f5289ffe51c7ba7d0f806d514e054d2112f0","0x73dd2e4bd4fcb71a7e96c2ff3f32f5289ffe51c7ba7d0f806d514e054d2112f0","0x77dbd85ebd0407f8ea0d104037593563b420c298eb508d93ee607b787dcc4c9f","0x77dbd85ebd0407f8ea0d104037593563b420c298eb508d93ee607b787dcc4c9f","0x7de11f4a32c502992abd430b33e5a2e04c964486bad27225743b4e8db45f879c","0x7de11f4a32c502992abd430b33e5a2e04c964486bad27225743b4e8db45f879c","0x8a3ec8b442215b93f37c7d8d5d242725601c6a1516249bba06a0828066d8e234","0x8d701e95b5cd642f2af23c0b79119d02a866b81102510048ff760d4970621cbf","0x8d701e95b5cd642f2af23c0b79119d02a866b81102510048ff760d4970621cbf","0x8f79ff4bc3c00e41d9e7938e09b787cb2f04d37d0f5e3d9034526aa3fcf22cf8","0xa5526f8bcc1c2b6a385a7dfea0a94d6e096f9a03d0eb9be53f1344b846e24b3a","0xbed169bbaa27a36ac84b937db896a7c89ab4197e5e621fc5698b904065106302","0xbed169bbaa27a36ac84b937db896a7c89ab4197e5e621fc5698b904065106302","0xc3e37274ed54ceef7d1dc3a8c0793521efc343725d532b134b21936ccbcbac60","0xc3e37274ed54ceef7d1dc3a8c0793521efc343725d532b134b21936ccbcbac60","0xcc7f12e24fbea878782325754897cead1cb7e1adca411059a95224644fb5fe6f","0xcea3b95bda5793e98163969774a48fac06f74263356e6f6e86d83c5476a49049","0xd05bbba765802e3344376cf264f1d373a7f29c4bfb984d14fedf13a6c9c6ee0a","0xd63298b6020838d684823c97748e393a69725abc82ac99355ea9eaa8ebae47cc","0xe0aac86b81387f28462a8253b3a1dbb12f3140f026d76fb2b333b51fbcd7dd06","0xe24514803343b5c56a8131ae8e4d8d77d75fe790b7cde70be5fd0519c66ca24a","0xe24514803343b5c56a8131ae8e4d8d77d75fe790b7cde70be5fd0519c66ca24a","0xe8f1ff4c190439abae59fef67936d3e0d2b5d6caa3d947829caf98fb16b85fb3","0xe8f1ff4c190439abae59fef67936d3e0d2b5d6caa3d947829caf98fb16b85fb3","0xefa1b41008026b075f549f673f3f48e75b6683690c4d3d5c45e1463dd7aec257","0xf3fc11e26c03f6cd7a1324bd95e6665efeb896b763a137bea9fd34b215f20d5b","0xf3fc11e26c03f6cd7a1324bd95e6665efeb896b763a137bea9fd34b215f20d5b","0xfcf4558f6432689ea57737fe63124a5ec39fd6ba6aaf198df13a825dd599bffc","0xfcf4558f6432689ea57737fe63124a5ec39fd6ba6aaf198df13a825dd599bffc","0xfcf4558f6432689ea57737fe63124a5ec39fd6ba6aaf198df13a825dd599bffc"]

def test_arbitrage():
    classifier = EventLogClassifier()
    pkl_file = open(f"{TEST_ARBITRAGES_DIRECTORY}/12914944.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    classified_event = classifier.classify(block.transactions)
    flashloans = get_flashloans(classified_event)
    swaps = get_swaps(classified_event)
    for sw in swaps:
        if sw.transaction_hash in reverted_transactions_of_12914944:
            reverted_transactions_of_12914944.remove(sw.transaction_hash)
        else:
            print(f"{sw.transaction_hash} not in  list")


    assert len(reverted_transactions_of_12914944) == 9

    assert len(swaps) == 43

    block_builder = get_block_builder(block.block.block.miner, block.block.network)

    arbitrages = get_arbitrages(list(swaps), flashloans)
    assert len(arbitrages) == 2

    arbitrage_1 = [
        arb
        for arb in arbitrages
        if arb.transaction_hash
        == "0x448245bf1a507b73516c4eeee01611927dada6610bf26d403012f2e66800d8f0"
    ][0]
    arbitrage_2 = [
        arb
        for arb in arbitrages
        if arb.transaction_hash
        == "0xfcf4558f6432689ea57737fe63124a5ec39fd6ba6aaf198df13a825dd599bffc"
    ][0]

    assert len(arbitrage_1.swaps) == 3
    assert (
        arbitrage_1.profit_token_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )
    assert len(arbitrage_1.swaps) == 3
    assert (
        arbitrage_1.swaps[1].token_in_address
        == "0x25f8087ead173b73d6e8b84329989a8eea16cf73"
    )
    assert (
        arbitrage_1.swaps[1].token_out_address
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    )
    assert arbitrage_1.profit_amount == 750005273675102326

    assert len(arbitrage_2.swaps) == 3
    assert (
        arbitrage_2.profit_token_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )
    assert len(arbitrage_2.swaps) == 3
    assert (
        arbitrage_2.swaps[1].token_in_address
        == "0x25f8087ead173b73d6e8b84329989a8eea16cf73"
    )
    assert (
        arbitrage_2.swaps[1].token_out_address
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    )
    assert arbitrage_2.profit_amount == 53560707941943273628



def test_flashloan_dxdy_swap_paraswap_zero_ex_arbitrage():
    swap_transaction = "0xc78e8ed4ecb43a7fd1c5d822009995c9fc426631e78b416773bae9057e6fc72f"
    classifier = EventLogClassifier()
    pkl_file = open(f"{TEST_ARBITRAGES_DIRECTORY}/16327006.pkl", 'rb')
    block: MevBlock = pickle.load(pkl_file)
    transactions = [t for t in block.transactions if t.hash == swap_transaction]
    block.transactions = transactions
    classified_event = classifier.classify(block.transactions)

    swaps = get_swaps(classified_event)
    flashloans = get_flashloans(classified_event)
    block_builder = get_block_builder(block.block.block.miner, block.block.network)

    arbitrages = get_arbitrages(list(swaps), flashloans)

    arbitrage_1 = [
        arb
        for arb in arbitrages
        if arb.transaction_hash
        == swap_transaction
    ][0]


    assert len(arbitrage_1.swaps) == 2
    assert (
        arbitrage_1.profit_token_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )

    assert arbitrage_1.profit_amount == 42412792772103669
