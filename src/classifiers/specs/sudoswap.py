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

SUDOSWAP_ABI_NAME = "sudoswap"


class SudoswapSwapInClassifier(SwapClassifier):
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
            token_out_address= ETH_TOKEN_ADDRESS,
            token_out_amount=event.inputs.get("amountOut"),
            error=event.error,
            owner_address= event.from_address
        )
        return swap

class SudoswapSwapOutClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        from_exchange_transfer:Transfer = None
        for t in transfers:
            if t.from_address == event.emitter_address and t.tokenId == event.inputs.get("ids")[0] :
                from_exchange_transfer = t

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
            token_in_address=ETH_TOKEN_ADDRESS,
            token_in_amount=event.inputs.get("amountIn"),
            token_in_id=-1,
            token_out_address=from_exchange_transfer.token_address,
            token_out_amount=1,
            token_out_id= from_exchange_transfer.tokenId,
            error=event.error,
            owner_address= event.from_address
        )
        return swap


SUDOSWAP_SPEC = ClassifierSpec(
    abi_name=SUDOSWAP_ABI_NAME,
    protocol=Protocol.sudoswap,
    classifiers={
        "SwapNFTInPair(uint256,uint256[])": SudoswapSwapInClassifier,
        "SwapNFTOutPair(uint256,uint256[])": SudoswapSwapOutClassifier,
    },
)

SUDOSWAP_CLASSIFIER_SPECS: List = [
    SUDOSWAP_SPEC
]


