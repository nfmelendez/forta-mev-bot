from typing import List, Optional

try:
    from src.schemas.classifiers import (
        ClassifierSpec,
        DecodedEvent,
        FlashLoanClassifier
    )
    from src.schemas.liquidations import Liquidation
    from src.schemas.events import Protocol, ClassifiedEvent
    from src.schemas.transfers import Transfer
    from src.schemas.flashloan import FlashLoan


except ModuleNotFoundError:
    from schemas.classifiers import (
        ClassifierSpec,
        DecodedEvent,
        FlashLoanClassifier
    )
    from schemas.liquidations import Liquidation
    from schemas.events import Protocol, ClassifiedEvent
    from schemas.transfers import Transfer
    from schemas.flashloan import FlashLoan


class MakerDAOFlashLoanClassifier(FlashLoanClassifier):
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
            target=flashloan.inputs["receiver"],
            initiator=flashloan.to_address,
            asset=flashloan.inputs["token"],
            amount=flashloan.inputs["amount"],
            to_address =flashloan.to_address
        )


MAKERDAO = ClassifierSpec(
    abi_name="makerdao",
    protocol=Protocol.makerdao,
    classifiers={
        "FlashLoan(address,address,uint256,uint256)": MakerDAOFlashLoanClassifier,
    },
)


MAKERDAO_CLASSIFIER_SPECS: List[ClassifierSpec] = [MAKERDAO]
