from typing import List, Optional, Sequence


try:
    from src.schemas.prices import ETH_TOKEN_ADDRESS
    from src.schemas.swaps import Swap
    from src.schemas.events import DecodedEvent
    from src.schemas.transfers import Transfer
except ModuleNotFoundError:
    from schemas.prices import ETH_TOKEN_ADDRESS
    from schemas.swaps import Swap
    from schemas.events import DecodedEvent
    from schemas.transfers import Transfer

def create_swap_from_pool_transfers(
    event: DecodedEvent,
    recipient_address: str,
    transfers: List[Transfer],
) -> Optional[Swap]:
    pool_address = event.emitter_address

    transfers_to_pool = []

    if len(transfers_to_pool) == 0:
        transfers_to_pool = _filter_transfers(transfers, to_address=pool_address)


    if len(transfers_to_pool) == 0:
        return None

    transfers_from_pool_to_recipient = _filter_transfers(
        transfers, to_address=recipient_address, from_address=pool_address
    )

    if len(transfers_from_pool_to_recipient) != 1:
        return None

    transfer_in = transfers_to_pool[-1]
    transfer_out = transfers_from_pool_to_recipient[0]

    if transfer_in.token_address == transfer_out.token_address:
        return None

    swap = Swap(
        abi_name=event.abi_name,
        transaction_hash=event.transaction_hash,
        transaction_position=event.transaction_position,
        block_number=event.block_number,
        log_index=event.log_index,
        contract_address=pool_address,
        protocol=event.protocol,
        from_address=transfer_in.from_address,
        to_address=transfer_out.to_address,
        token_in_address=transfer_in.token_address,
        token_in_amount=transfer_in.amount,
        token_out_address=transfer_out.token_address,
        token_out_amount=transfer_out.amount,
        error=event.error,
        owner_address= event.from_address
    )

    return swap


def filter_transfers(
    transfers: Sequence[Transfer],
    to_address: Optional[str] = None,
    from_address: Optional[str] = None,
) -> List[Transfer]:
    return _filter_transfers(transfers, to_address, from_address)

def _filter_transfers(
    transfers: Sequence[Transfer],
    to_address: Optional[str] = None,
    from_address: Optional[str] = None,
) -> List[Transfer]:
    filtered_transfers = []

    for transfer in transfers:
        if to_address is not None and transfer.to_address != to_address:
            continue

        if from_address is not None and transfer.from_address != from_address:
            continue

        filtered_transfers.append(transfer)

    return filtered_transfers
