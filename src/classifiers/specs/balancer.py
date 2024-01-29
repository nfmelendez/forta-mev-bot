from typing import List, Optional

try:
    from src.classifiers.helpers import create_swap_from_pool_transfers
    from src.schemas.classifiers import ClassifierSpec, SwapClassifier, FlashLoanClassifier
    from src.schemas.swaps import Swap
    from src.schemas.events import Protocol, DecodedEvent
    from src.schemas.transfers import Transfer
    from src.schemas.flashloan import FlashLoan
except ModuleNotFoundError:
    from classifiers.helpers import create_swap_from_pool_transfers
    from schemas.classifiers import ClassifierSpec, SwapClassifier, FlashLoanClassifier
    from schemas.swaps import Swap
    from schemas.events import Protocol, DecodedEvent
    from schemas.transfers import Transfer
    from schemas.flashloan import FlashLoan

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

class BalancerFlashLoanClassifier(FlashLoanClassifier):
    @staticmethod
    def parse_flashloan(
        flashloan: DecodedEvent,
        transfers: List[Transfer]
    ) -> Optional[FlashLoan]:
        
        return FlashLoan(
            abi_name= flashloan.abi_name,
            transaction_position= flashloan.transaction_position,
            contract_address=flashloan.emitter_address,
            from_address=flashloan.from_address,
            protocol=Protocol.makerdao,
            transaction_hash=flashloan.transaction_hash,
            log_index=flashloan.log_index,
            block_number=flashloan.block_number,
            error=flashloan.error,
            target=flashloan.inputs["recipient"],
            initiator=flashloan.to_address,
            asset=flashloan.inputs["token"],
            amount=flashloan.inputs["amount"],
            to_address =flashloan.to_address
        )


BLANCER_SPEC = ClassifierSpec(
    abi_name=BALANCER_ABI_NAME,
    protocol=Protocol.balancer,
    classifiers={
        "Swap(bytes32,address,address,uint256,uint256)": BalancerSwapClassifier,
        "FlashLoan(address,address,uint256,uint256)": BalancerFlashLoanClassifier,
    },
)

#Order is importan from from specific to general. for example first sushiswap, then all v2 uniswap copycats
BALANCER_CLASSIFIER_SPECS: List = [
    BLANCER_SPEC,
]

