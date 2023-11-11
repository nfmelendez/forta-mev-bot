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

BALANCER_ABI_NAME = "balancer"

class BalancerSwapClassifier(SwapClassifier):
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



BLANCER_SPEC = ClassifierSpec(
    abi_name=BALANCER_ABI_NAME,
    protocol=Protocol.balancer,
    classifiers={
        "Swap(bytes32,address,address,uint256,uint256)": BalancerSwapClassifier,
    },
)

#Order is importan from from specific to general. for example first sushiswap, then all v2 uniswap copycats
BALANCER_CLASSIFIER_SPECS: List = [
    BLANCER_SPEC,
]

