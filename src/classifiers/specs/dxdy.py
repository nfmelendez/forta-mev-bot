from typing import List, Optional

try:
    from src.schemas.classifiers import (
        ClassifierSpec,
        LiquidationClassifier,
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
        LiquidationClassifier,
        DecodedEvent,
        FlashLoanClassifier
    )
    from schemas.liquidations import Liquidation
    from schemas.events import Protocol, ClassifiedEvent
    from schemas.transfers import Transfer
    from schemas.flashloan import FlashLoan


class AaveV2FlashLoanClassifier(FlashLoanClassifier):
    @staticmethod
    def parse_flashloan(
        flashloan: DecodedEvent,
        transfers: List[Transfer]
    ) -> Optional[FlashLoan]:
        
        try:
            from src.transfers import filter_transfers
        except ModuleNotFoundError:
            from transfers import filter_transfers
     
        accountOwner = flashloan.inputs["accountOwner"]
        to = flashloan.inputs["to"]
        ts = filter_transfers(transfers, to, flashloan.emitter_address)
        if not ts:
            return None
        t = ts[-1]
        return FlashLoan(
            abi_name= flashloan.abi_name,
            transaction_position= flashloan.transaction_position,
            contract_address=flashloan.emitter_address,
            from_address=flashloan.from_address,
            protocol=Protocol.dxdy,
            transaction_hash=flashloan.transaction_hash,
            log_index=flashloan.log_index,
            block_number=flashloan.block_number,
            error=flashloan.error,
            target=to,
            initiator=accountOwner,
            asset=t.token_address,
            amount=t.amount,
            to_address =flashloan.to_address
        )


AAVE_SPEC_V2 = ClassifierSpec(
    abi_name="dxdy",
    protocol=Protocol.dxdy,
    classifiers={
        "LogWithdraw(address,uint256,uint256,((bool,uint256),(bool,uint128)),address)": AaveV2FlashLoanClassifier,
    },
)


DXDY_CLASSIFIER_SPECS: List[ClassifierSpec] = [AAVE_SPEC_V2]


# [
#             {
#                 "indexed": true,
#                 "name": "accountOwner",
#                 "type": "address"
#             },
#             {
#                 "indexed": false,
#                 "name": "accountNumber",
#                 "type": "uint256"
#             },
#             {
#                 "indexed": false,
#                 "name": "market",
#                 "type": "uint256"
#             },
#             {
#                 "components": [
#                     {
#                         "components": [
#                             {
#                                 "name": "sign",
#                                 "type": "bool"
#                             },
#                             {
#                                 "name": "value",
#                                 "type": "uint256"
#                             }
#                         ],
#                         "name": "deltaWei",
#                         "type": "tuple"
#                     },
#                     {
#                         "components": [
#                             {
#                                 "name": "sign",
#                                 "type": "bool"
#                             },
#                             {
#                                 "name": "value",
#                                 "type": "uint128"
#                             }
#                         ],
#                         "name": "newPar",
#                         "type": "tuple"
#                     }
#                 ],
#                 "indexed": false,
#                 "name": "update",
#                 "type": "tuple"
#             },
#             {
#                 "indexed": false,
#                 "name": "to",
#                 "type": "address"
#             }
#         ]