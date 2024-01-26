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


class EventCurvefiSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        buyer = event.inputs.get("buyer")
        in_transfer = None
        out_transfer = None

        for t in transfers:
            if t.from_address == buyer and t.amount == event.inputs.get("tokens_sold"):
                in_transfer = t
            if t.to_address == buyer and t.amount == event.inputs.get("tokens_bought"):
                out_transfer = t

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
            token_in_address=in_transfer.token_address,
            token_in_amount=in_transfer.amount,
            token_out_address=out_transfer.token_address,
            token_out_amount=out_transfer.amount,
            error=event.error,
            owner_address= event.from_address
        )
        return swap


CURVEFI = ClassifierSpec(
    abi_name="curvefi",
    protocol=Protocol.curvefi,
    classifiers={
        "TokenExchange(address,int128,uint256,int128,uint256)": EventCurvefiSwapClassifier,
    },
)


CURVEFI_CLASSIFIER_SPECS: List[ClassifierSpec] = [CURVEFI]

