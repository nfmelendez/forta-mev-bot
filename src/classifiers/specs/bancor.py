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

        swap = Swap(
            abi_name=event.abi_name,
            transaction_hash=event.transaction_hash,
            transaction_position=event.transaction_position,
            block_number=event.block_number,
            log_index=event.log_index,
            contract_address=event.emitter_address,
            protocol=event.protocol,
            from_address=event.inputs.get("_trader"),
            to_address=event.inputs.get("_trader"),
            token_in_address=event.inputs.get("_fromToken"),
            token_in_amount=event.inputs.get("_amount"),
            token_out_address=event.inputs.get("_toToken"),
            token_out_amount=event.inputs.get("_return"),
            error=event.error,
            owner_address= event.from_address
        )
        return swap

class BancorV3SwapClassifier(SwapClassifier):
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
            from_address=event.inputs.get("trader"),
            to_address=event.inputs.get("trader"),
            token_in_address=event.inputs.get("sourceToken"),
            token_in_amount=event.inputs.get("sourceAmount"),
            token_out_address=event.inputs.get("targetToken"),
            token_out_amount=event.inputs.get("targetAmount"),
            error=event.error,
            owner_address= event.from_address
        )
        return swap


BANCOR_V2_SPEC = ClassifierSpec(
    abi_name=BANCOR_V2_ABI_NAME,
    protocol=Protocol.bancor,
    classifiers={
        "Conversion(address,address,address,uint256,uint256,int256)": BancorV2SwapClassifier,
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


