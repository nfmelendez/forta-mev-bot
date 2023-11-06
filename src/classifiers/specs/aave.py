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


class AaveLiquidationClassifier(LiquidationClassifier):
    @staticmethod
    def parse_liquidation(
        liquidation_event: DecodedEvent,
        transfer_events: List[ClassifiedEvent]
    ) -> Optional[Liquidation]:
        
        from src.transfers import (
            get_transfers,
            filter_transfers
        )

        receive_a_token = liquidation_event.inputs["receiveAToken"]
        liquidator = liquidation_event.inputs["liquidator"]
        liquidated = liquidation_event.inputs["user"]

        debt_token_address = liquidation_event.inputs["debtAsset"]

        if receive_a_token: 
            transfers = get_transfers(transfer_events)
            atoken_transfer = filter_transfers(transfers, liquidator, liquidated)
            received_token_address = atoken_transfer[0].token_address

        else:
            received_token_address = liquidation_event.inputs["collateralAsset"]

        debt_purchase_amount = liquidation_event.inputs["debtToCover"]

        received_amount = liquidation_event.inputs["liquidatedCollateralAmount"]
        error = None
        if liquidation_event.error != '':
            error = liquidation_event.error 

        return Liquidation(
            liquidated_user=liquidated,
            debt_token_address=debt_token_address,
            liquidator_user=liquidator,
            debt_purchase_amount=debt_purchase_amount,
            protocol=Protocol.aave,
            received_amount=received_amount,
            received_token_address=received_token_address,
            transaction_hash=liquidation_event.transaction_hash,
            log_index=liquidation_event.log_index,
            block_number=liquidation_event.block_number,
            error=error,
            receive_a_token=receive_a_token,
            bot_owner= liquidation_event.from_address
        )


class AaveV2FlashLoanClassifier(FlashLoanClassifier):
    @staticmethod
    def parse_flashloan(
        flashloan: DecodedEvent,
    ) -> Optional[FlashLoan]:
        
        return FlashLoan(
            abi_name= flashloan.abi_name,
            transaction_position= flashloan.transaction_position,
            contract_address=flashloan.emitter_address,
            from_address=flashloan.from_address,
            protocol=Protocol.aave,
            transaction_hash=flashloan.transaction_hash,
            log_index=flashloan.log_index,
            block_number=flashloan.block_number,
            error=flashloan.error,
            target=flashloan.inputs["target"],
            initiator=flashloan.inputs["initiator"],
            asset=flashloan.inputs["asset"],
            amount=flashloan.inputs["amount"],
            premium=flashloan.inputs["premium"],
            referralCode=flashloan.inputs["referralCode"],
            to_address =flashloan.to_address
        )


AAVE_SPEC_V2 = ClassifierSpec(
    abi_name="AaveV2",
    protocol=Protocol.aave,
    classifiers={
        "LiquidationCall(address,address,address,uint256,uint256,address,bool)": AaveLiquidationClassifier,
        "FlashLoan(address,address,address,uint256,uint256,uint16)": AaveV2FlashLoanClassifier,
    },
)


AAVE_CLASSIFIER_SPECS: List[ClassifierSpec] = [AAVE_SPEC_V2]

