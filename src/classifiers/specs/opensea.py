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


# Sea port documentation
# https://github.com/ProjectOpenSea/seaport/blob/main/docs/SeaportDocumentation.md

SEAPORT15_ABI_NAME = "seaport15"



class OpenSeaSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

# Ether (or other native token for the given chain) enum value: NATIVE = 0
# ERC20: enum value: ERC20 = 1
# ERC721: enum value: ERC721 = 2

        offer_type =  event.inputs.get("offer")[0][0]
        if (offer_type == 2):
            token_out_address= event.inputs.get("offer")[0][1]
            token_out_amount=event.inputs.get("offer")[0][3]
            token_out_id=event.inputs.get("offer")[0][2]
            token_in_address = event.inputs.get("consideration")[0][1]
            token_in_amount = 0
            for _ , consideration in enumerate(event.inputs.get("consideration")):
                token_in_amount += consideration[3]

            # is native blockchain token
            if(token_in_address == "0x0000000000000000000000000000000000000000"):
                token_in_address = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
                
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
            token_in_address=token_in_address,
            token_in_amount=token_in_amount,
            token_out_address= token_out_address,
            token_out_amount=token_out_amount,
            token_out_id=token_out_id,
            error=event.error,
            owner_address= event.from_address
        )
        return swap




SEAPORT15_SPEC = ClassifierSpec(
    abi_name=SEAPORT15_ABI_NAME,
    protocol=Protocol.opensea,
    classifiers={
        "OrderFulfilled(bytes32,address,address,address,(uint8,address,uint256,uint256)[],(uint8,address,uint256,uint256,address)[])": OpenSeaSwapClassifier,
    },
)

OPENSEA_CLASSIFIER_SPECS: List = [
    SEAPORT15_SPEC
]


