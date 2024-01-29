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


class DODOFlashLoanClassifier(FlashLoanClassifier):
    @staticmethod
    def parse_flashloan(
        flashloan: DecodedEvent,
        transfers: List[Transfer]
    ) -> Optional[FlashLoan]:
        
        asset = None
        amount = flashloan.inputs["quoteAmount"]

        out_transfer = None

        for t in transfers:
            if flashloan.emitter_address == t.from_address and t.amount == amount:
                out_transfer = t

        if out_transfer == None:
            return None
        asset = out_transfer.token_address
        return FlashLoan(
            abi_name= flashloan.abi_name,
            transaction_position= flashloan.transaction_position,
            contract_address=flashloan.emitter_address,
            from_address=flashloan.from_address,
            protocol=Protocol.dodo,
            transaction_hash=flashloan.transaction_hash,
            log_index=flashloan.log_index,
            block_number=flashloan.block_number,
            error=flashloan.error,
            target=flashloan.inputs["assetTo"],
            initiator=flashloan.inputs["borrower"],
            asset=asset,
            amount=amount,
            to_address =flashloan.to_address
        )


DODO = ClassifierSpec(
    abi_name="dodo",
    protocol=Protocol.dodo,
    classifiers={
        "DODOFlashLoan(address,address,uint256,uint256)": DODOFlashLoanClassifier,
    },
)


DODO_CLASSIFIER_SPECS: List[ClassifierSpec] = [DODO]
