from typing import List, Optional
import pickle

try:
    from src.classifiers.helpers import create_swap_from_pool_transfers
    from src.schemas.classifiers import ClassifierSpec, SwapClassifier, TransferClassifier
    from src.schemas.swaps import Swap
    from src.schemas.events import Protocol, DecodedEvent
    from src.schemas.transfers import Transfer
    from src.schemas.prices import ETH_TOKEN_ADDRESS
    from src.schemas.transfers import Transfer
except ModuleNotFoundError:
    from classifiers.helpers import create_swap_from_pool_transfers
    from schemas.classifiers import ClassifierSpec, SwapClassifier, TransferClassifier
    from schemas.swaps import Swap
    from schemas.events import Protocol, DecodedEvent
    from schemas.transfers import Transfer
    from schemas.prices import ETH_TOKEN_ADDRESS
    from schemas.transfers import Transfer

NFTX_ABI_NAME = "nftx"

# Swap in and out from perfective of opensea protocol
class NFTXSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        event: DecodedEvent,
        transfers: List[Transfer],
    ) -> Optional[Swap]:

        token_out_address= ETH_TOKEN_ADDRESS
        token_out_amount=event.inputs.get("ethReceived")
        token_out_id=-1

        nftx_minter = [trans for trans in transfers if trans.to_address == event.emitter_address and trans.tokenId != -1]
        if nftx_minter == None or len(nftx_minter) != 1:
            print("NFTX error: nftx minter should be 1")
            return None

        nftx_receiver = [trans for trans in transfers if trans.to_address == nftx_minter[0].from_address and trans.tokenId == nftx_minter[0].tokenId]

        if nftx_receiver == None or len(nftx_receiver) != 1:
            print("NFTX error: nftx receiver should be 1")
            return None
        
        token_in_address = nftx_receiver[0].token_address
        token_in_amount = 1
        token_in_id = nftx_minter[0].tokenId
   
             
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

class NFTXVaultTransferClassifier(TransferClassifier):
    @staticmethod
    def get_transfer(event: DecodedEvent) -> Transfer:
        nftIds = event.inputs["nftIds"]
        if len(nftIds) >= 2:
            print(f"Error in NFTX mint convertion to transfer, nftIds are more then 1, {len(nftIds)}")
            return None
        return Transfer(
            block_number=event.block_number,
            transaction_hash=event.transaction_hash,
            log_index= event.log_index,
            amount= 1,
            tokenId=event.inputs["nftIds"][0],
            to_address=event.inputs["to"],
            from_address=event.emitter_address,
            token_address=event.emitter_address,
        )



NFTX_SPEC = ClassifierSpec(
    abi_name=NFTX_ABI_NAME,
    protocol=Protocol.nftx,
    classifiers={
        "Sell(uint256,uint256,address)": NFTXSwapClassifier,
    },
)

NFTX_VAULT_SPEC = ClassifierSpec(
    abi_name="nftx_vault_upgradeable",
    protocol=Protocol.nftx,
    classifiers={
        "Minted(uint256[],uint256[],address)": NFTXVaultTransferClassifier,
    },
)
NFTX_CLASSIFIER_SPECS: List = [
    NFTX_VAULT_SPEC,
    NFTX_SPEC
]


