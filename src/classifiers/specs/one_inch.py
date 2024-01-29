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


class Event1inchSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        maker = event.inputs.get("maker")
        in_transfer = None
        out_transfer = None

        for t in transfers:
            if t.from_address == maker:
                out_transfer = t
            if t.to_address == maker:
                in_transfer = t

        if in_transfer == None or out_transfer == None:
            return None
        
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


ONEINCH = ClassifierSpec(
    abi_name="one_inch",
    protocol=Protocol.oneinch,
    classifiers={
        "OrderFilled(address,bytes32,uint256)": Event1inchSwapClassifier,
    },
)


ONEINCH_CLASSIFIER_SPECS: List[ClassifierSpec] = [ONEINCH]

