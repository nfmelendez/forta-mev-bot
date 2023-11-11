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

BALANCER_ABI_NAME = "zero_ex"

class BalancerSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        recipient_address = event.inputs.get("taker", event.to_address)

        swap = Swap(
            abi_name=event.abi_name,
            transaction_hash=event.transaction_hash,
            transaction_position=event.transaction_position,
            block_number=event.block_number,
            log_index=event.log_index,
            contract_address=event.emitter_address,
            protocol=event.protocol,
            from_address=recipient_address,
            to_address=recipient_address,
            token_in_address= event.inputs.get("inputToken"),
            token_in_amount=event.inputs.get("inputTokenAmount"),
            token_out_address=event.inputs.get("outputToken"),
            token_out_amount=event.inputs.get("outputTokenAmount"),
            error=event.error,
            owner_address= event.from_address
        )
        return swap



BLANCER_SPEC = ClassifierSpec(
    abi_name=BALANCER_ABI_NAME,
    protocol=Protocol.zero_ex,
    classifiers={
        "TransformedERC20(address,address,address,uint256,uint256)": BalancerSwapClassifier,
    },
)

#Order is importan from from specific to general. for example first sushiswap, then all v2 uniswap copycats
ZEROEX_CLASSIFIER_SPECS: List = [
    BLANCER_SPEC,
]

