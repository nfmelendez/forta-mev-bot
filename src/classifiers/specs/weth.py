from typing import List, Optional

try:
    from src.classifiers.helpers import create_swap_from_pool_transfers
    from src.schemas.classifiers import ClassifierSpec, SwapClassifier
    from src.schemas.swaps import Swap
    from src.schemas.events import Protocol, DecodedEvent
    from src.schemas.transfers import Transfer
    from src.schemas.prices import ETH_TOKEN_ADDRESS
except ModuleNotFoundError:
    from classifiers.helpers import create_swap_from_pool_transfers
    from schemas.classifiers import ClassifierSpec, SwapClassifier
    from schemas.swaps import Swap
    from schemas.events import Protocol, DecodedEvent
    from schemas.transfers import Transfer
    from schemas.prices import ETH_TOKEN_ADDRESS

WETH_ABI_NAME = "weth"


class WethSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:


        swap = Swap(
            abi_name=event.abi_name,
            transaction_hash=event.transaction_hash,
            transaction_position=event.transaction_position,
            block_number=event.block_number,
            log_index=event.log_index,
            contract_address=event.emitter_address,
            protocol=event.protocol,
            from_address=event.to_address,
            to_address=event.to_address,
            token_in_address=event.emitter_address,
            token_in_amount=event.inputs.get("wad"),
            token_out_address= ETH_TOKEN_ADDRESS,
            token_out_amount=event.inputs.get("wad"),
            error=event.error,
            owner_address= event.from_address
        )
        return swap




WETH_SPEC = ClassifierSpec(
    abi_name=WETH_ABI_NAME,
    protocol=Protocol.weth,
    classifiers={
        "Withdrawal(address,uint256)": WethSwapClassifier,
    },
)




WETH_CLASSIFIER_SPECS: List = [
    WETH_SPEC
]


