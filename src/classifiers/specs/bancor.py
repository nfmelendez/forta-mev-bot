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

BANCOR_V2_ABI_NAME = "bancorv2"
BANCOR_V3_ABI_NAME = "bancorv3"

class BancorV2SwapClassifier(SwapClassifier):
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

class BancorV3SwapClassifier(SwapClassifier):
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


BANCOR_V2_SPEC = ClassifierSpec(
    abi_name=BANCOR_V2_ABI_NAME,
    protocol=Protocol.bancor,
    classifiers={
        "Conversion(address,address,address,uint256,uint256,address)": BancorV2SwapClassifier,
    },
)

BANCOR_V3_SPEC = ClassifierSpec(
    abi_name=BANCOR_V3_ABI_NAME,
    protocol=Protocol.bancor,
    classifiers={
        "TokensTraded(bytes32,address,address,uint256,uint256,uint256,uint256,uint256,address)": BancorV3SwapClassifier,
    },
)




BANCOR_CLASSIFIER_SPECS: List = [
    BANCOR_V2_SPEC,
    BANCOR_V3_SPEC
]


