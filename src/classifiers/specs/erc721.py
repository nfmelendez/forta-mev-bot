
try:
    from src.schemas.classifiers import ClassifierSpec, TransferClassifier
    from src.schemas.events import DecodedEvent
    from src.schemas.transfers import Transfer
except ModuleNotFoundError:
    from schemas.classifiers import ClassifierSpec, TransferClassifier
    from schemas.events import DecodedEvent
    from schemas.transfers import Transfer

class ERC721TransferClassifier(TransferClassifier):
    @staticmethod
    def get_transfer(event: DecodedEvent) -> Transfer:
        return Transfer(
            block_number=event.block_number,
            transaction_hash=event.transaction_hash,
            log_index= event.log_index,
            amount= 1,
            tokenId=event.inputs["tokenId"],
            to_address=event.inputs["to"],
            from_address=event.inputs.get("from", event.from_address),
            token_address=event.emitter_address,
        )


_ERC721_SPEC = ClassifierSpec(
    abi_name="ERC721",
    classifiers={
        "Transfer(address,address,uint256)": ERC721TransferClassifier
    },
)

ERC721_CLASSIFIER_SPECS = [_ERC721_SPEC]
