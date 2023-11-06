
try:
    from src.schemas.classifiers import ClassifierSpec, TransferClassifier
    from src.schemas.events import DecodedEvent
    from src.schemas.transfers import Transfer
except ModuleNotFoundError:
    from schemas.classifiers import ClassifierSpec, TransferClassifier
    from schemas.events import DecodedEvent
    from schemas.transfers import Transfer

class ERC20TransferClassifier(TransferClassifier):
    @staticmethod
    def get_transfer(event: DecodedEvent) -> Transfer:
        return Transfer(
            block_number=event.block_number,
            transaction_hash=event.transaction_hash,
            log_index= event.log_index,
            amount=event.inputs["value"],
            to_address=event.inputs["to"],
            from_address=event.inputs.get("from", event.from_address),
            token_address=event.emitter_address,
        )


ERC20_SPEC = ClassifierSpec(
    abi_name="ERC20",
    classifiers={
        "Transfer(address,address,uint256)": ERC20TransferClassifier
    },
)

ERC20_CLASSIFIER_SPECS = [ERC20_SPEC]
