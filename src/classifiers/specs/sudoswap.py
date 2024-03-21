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

SUDOSWAP_ABI_NAME = "sudoswap"


class SudoswapSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        to_exchange_transfer:Transfer = None
        for t in transfers:
            if t.to_address == event.emitter_address:
                to_exchange_transfer = t

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
            token_in_address=to_exchange_transfer.token_address,
            token_in_amount=1,
            token_in_id=event.inputs.get("ids")[0],
            token_out_address= "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            token_out_amount=event.inputs.get("amountOut"),
            error=event.error,
            owner_address= event.from_address
        )
        return swap




SUDOSWAP_SPEC = ClassifierSpec(
    abi_name=SUDOSWAP_ABI_NAME,
    protocol=Protocol.sudoswap,
    classifiers={
        "SwapNFTInPair(uint256,uint256[])": SudoswapSwapClassifier,
    },
)

SUDOSWAP_CLASSIFIER_SPECS: List = [
    SUDOSWAP_SPEC
]


