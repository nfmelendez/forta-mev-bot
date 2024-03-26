from typing import List, Optional
import pickle

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


# Sea port documentation
# https://github.com/ProjectOpenSea/seaport/blob/main/docs/SeaportDocumentation.md

SEAPORT15_ABI_NAME = "seaport15"

OFFER_TYPE = 0


# Swap in and out from perfective of opensea protocol
class OpenSeaSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

# Ether (or other native token for the given chain) enum value: NATIVE = 0
# ERC20: enum value: ERC20 = 1
# ERC721: enum value: ERC721 = 2
        


        offer_type =  event.inputs.get("offer")[0][OFFER_TYPE]

        if (offer_type == 1 or offer_type == 0):
            token_out_address = event.inputs.get("offer")[0][1]
            token_out_amount = event.inputs.get("offer")[0][3]
            token_out_id = -1
        elif (offer_type == 2 or offer_type == 3):
            token_out_address= event.inputs.get("offer")[0][1]
            token_out_amount=event.inputs.get("offer")[0][3]
            token_out_id=event.inputs.get("offer")[0][2]
        else:
            return None

        selected_consideration = None
        for _ , consideration in enumerate(event.inputs.get("consideration")):
            if consideration[4] == event.inputs.get("offerer"):
                selected_consideration = consideration
                break 
        
        if not selected_consideration:
            return None

        if (selected_consideration[0] == 0 or selected_consideration[0] == 1):
            token_in_address = selected_consideration[1]
            if (token_in_address == "0x0000000000000000000000000000000000000000"):
                token_in_address = ETH_TOKEN_ADDRESS
            token_in_address= token_in_address
            token_in_amount= selected_consideration[3]
            token_in_id=-1

        elif (selected_consideration[0] == 2 or selected_consideration[0] == 3):
            token_in_address = selected_consideration[1]
            token_in_amount = 1
            token_in_id = selected_consideration[2]
        else:
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
            token_in_address=token_in_address,
            token_in_amount=token_in_amount,
            token_in_id=token_in_id,
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


