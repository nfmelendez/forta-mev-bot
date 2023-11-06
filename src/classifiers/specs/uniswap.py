from typing import List, Optional

try:
    from src.classifiers.helpers import create_swap_from_pool_transfers
    from src.schemas.classifiers import ClassifierSpec, SwapClassifier
    from src.schemas.swaps import Swap
    from src.schemas.events import Protocol, DecodedEvent
    from src.schemas.transfers import Transfer
except ModuleNotFoundError:
    from classifiers.helpers import create_swap_from_pool_transfers
    from schemas.classifiers import ClassifierSpec, SwapClassifier
    from schemas.swaps import Swap
    from schemas.events import Protocol, DecodedEvent
    from schemas.transfers import Transfer

UNISWAP_V2_PAIR_ABI_NAME = "UniswapV2Pair"
UNISWAP_V3_POOL_ABI_NAME = "UniswapV3Pool"

class EventUniswapV3SwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        recipient_address = event.inputs.get("recipient", event.from_address)

        swap = create_swap_from_pool_transfers(
            event, recipient_address, transfers
        )
        return swap

class UniswapV2SwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        recipient_address = event.inputs.get("to", event.from_address)

        swap = create_swap_from_pool_transfers(
            event, recipient_address, transfers
        )
        return swap


UNISWAP_V3_GENERAL_SPECS = ClassifierSpec(
        abi_name=UNISWAP_V3_POOL_ABI_NAME,
        protocol=Protocol.uniswap_v3,
        classifiers={
            "Swap(address,address,int256,int256,uint160,uint128,int24)": EventUniswapV3SwapClassifier
        },
    )




UNISWAPPY_V2_PAIR_SPEC = ClassifierSpec(
    abi_name=UNISWAP_V2_PAIR_ABI_NAME,
    protocol=Protocol.uniswap_v2,
    classifiers={
        "Swap(address,uint256,uint256,uint256,uint256,address)": UniswapV2SwapClassifier,
    },
)

SUSHISWAPPY_V2_PAIR_SPEC = ClassifierSpec(
    abi_name=UNISWAP_V2_PAIR_ABI_NAME,
    protocol=Protocol.sushiswap,
    classifiers={
        "Swap(address,uint256,uint256,uint256,uint256,address)": UniswapV2SwapClassifier,
    },
    valid_contract_addresses=["0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"],
)

#Order is importan from from specific to general. for example first sushiswap, then all v2 uniswap copycats
UNISWAP_CLASSIFIER_SPECS: List = [
    UNISWAP_V3_GENERAL_SPECS,
    SUSHISWAPPY_V2_PAIR_SPEC,
    UNISWAPPY_V2_PAIR_SPEC,
]
