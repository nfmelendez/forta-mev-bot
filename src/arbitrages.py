from itertools import groupby
from typing import List, Optional, Tuple
import logging


try:
    from src.schemas.arbitrages import Arbitrage
    from src.schemas.swaps import Swap
    from src.flashloans import get_flashloans
    from src.schemas.flashloan import FlashLoan
except ModuleNotFoundError:
    from schemas.arbitrages import Arbitrage
    from schemas.swaps import Swap
    from schemas.flashloan import FlashLoan

TOKEN_AMOUNT_THRESHOLD_PERCENT = 0.01


def get_arbitrages(swaps: List[Swap], flashloans: List[FlashLoan]) -> List[Arbitrage]:
    """
    There are 2 cases:
    1) Chain which is BOT -> A/B -> B/C -> C/A -> BOT
    2) Atomic swaps that return each time to the BOT,  which is BOT -> A/B -> BOT -> B/C -> BOT -> A/C -> BOT
    """
    get_transaction_hash = lambda element: element.transaction_hash
    swaps_by_transaction = groupby(
        sorted(swaps, key=get_transaction_hash),
        key=get_transaction_hash,
    )

    flashloans_by_transaction = groupby(
        sorted(flashloans, key=get_transaction_hash),
        key=get_transaction_hash,
    )

    transaction_hash_per_flashloan = {}
    for flashloan_transaction_hash, transaction_flashloan in flashloans_by_transaction:
        transaction_hash_per_flashloan[flashloan_transaction_hash] = list(transaction_flashloan)

    all_arbitrages = []

    for transaction_hash, transaction_swaps in swaps_by_transaction:
        all_arbitrages += _get_arbitrages(
            list(transaction_swaps),
            transaction_hash_per_flashloan.get(transaction_hash),
        )

    return all_arbitrages


def _get_arbitrages(swaps: List[Swap], flashloans: List[FlashLoan]) -> List[Arbitrage]:


    arbitrages = []

    # Gets the set of all possible openings and closing swaps for an arbitrage 
    head_tails = _get_head_tail_swaps(swaps)
    if not head_tails:
        return []

    used_swaps: List[Swap] = []

    for (head, tails) in head_tails:
        if head in used_swaps:
            continue

        unused_tails = [tail for tail in tails if tail not in used_swaps]
        chain = _get_shortest_chain(head, unused_tails, swaps)

        if chain is not None:
            first_chain = chain[0]
            head_amount = first_chain.token_in_amount
            tail_amount = chain[-1].token_out_amount
            profit_amount = tail_amount - head_amount
            error = None
            for swap in chain:
                if swap.error is not None:
                    error = swap.error

            flashloan = None
            if flashloans:
                flashloan = flashloans[0]
            arb = Arbitrage(
                swaps=chain,
                block_number=first_chain.block_number,
                transaction_hash=first_chain.transaction_hash,
                account_address=first_chain.from_address,
                profit_token_address=first_chain.token_in_address,
                start_amount=head_amount,
                end_amount=tail_amount,
                profit_amount=profit_amount,
                error=error,
                flashloan=flashloan
            )

            arbitrages.append(arb)
            used_swaps.extend(chain)

    if not arbitrages:
        return []
    
    if len(arbitrages) > 1:
        return _multiple_arbitrages(arbitrages)
    else:
        return arbitrages


def _multiple_arbitrages(arbitrages:List[Arbitrage]) -> List[Arbitrage]:
    logging.info(f"Multiple ({len(arbitrages)}) swap chain founds in transaction: {arbitrages[0].transaction_hash}")
    return [
            arb
            for arb in arbitrages
            if (arb.swaps[0].log_index < arb.swaps[-1].log_index)
        ]

def _get_shortest_chain(
    head_swap: Swap,
    tail_swaps: List[Swap],
    all_swaps: List[Swap],
    max_chain_length: Optional[int] = None,
) -> Optional[List[Swap]]:
    if len(tail_swaps) == 0:
        return None

    if max_chain_length is not None and max_chain_length < 2:
        return None

    for tail_swap in tail_swaps:
        if _swap_outs_match_swap_ins(head_swap, tail_swap):
            return [head_swap, tail_swap]

    if max_chain_length is not None and max_chain_length == 2:
        return None

    other_swaps = [
        swap for swap in all_swaps if (swap is not head_swap and swap not in tail_swaps)
    ]

    if not other_swaps:
        return None

    shortest_remaining_chain = None
    max_remaining_chain_length = (
        None if max_chain_length is None else max_chain_length - 1
    )

    for next_swap in other_swaps:
        if _swap_outs_match_swap_ins(head_swap, next_swap):
            shortest_from_next = _get_shortest_chain(
                next_swap,
                tail_swaps,
                other_swaps,
                max_chain_length=max_remaining_chain_length,
            )

            if shortest_from_next is not None and (
                shortest_remaining_chain is None
                or len(shortest_from_next) < len(shortest_remaining_chain)
            ):
                shortest_remaining_chain = shortest_from_next
                max_remaining_chain_length = len(shortest_from_next) - 1

    if shortest_remaining_chain is None:
        return None
    else:
        return [head_swap] + shortest_remaining_chain


def _get_head_tail_swaps(swaps: List[Swap]) -> List[Tuple[Swap, List[Swap]]]:
    pool_address = [swap.contract_address for swap in swaps]
    valid_head_tails: List[Tuple[Swap, List[Swap]]] = []

    for index, head_swap_candidate in enumerate(swaps):
        tails_for_head: List[Swap] = []
        remaining_swaps = swaps[:index] + swaps[index + 1 :]

        for tail_swap_candidate in remaining_swaps:
            if (
                head_swap_candidate.token_in_address
                == tail_swap_candidate.token_out_address
                and head_swap_candidate.contract_address
                != tail_swap_candidate.contract_address
                and head_swap_candidate.from_address == tail_swap_candidate.to_address
                and not head_swap_candidate.from_address in pool_address
            ):

                tails_for_head.append(tail_swap_candidate)

        if len(tails_for_head) > 0:
            valid_head_tails.append((head_swap_candidate, tails_for_head))

    return valid_head_tails


def _swap_outs_match_swap_ins(swap_out, swap_in) -> bool:
    return (
        swap_out.token_out_address == swap_in.token_in_address
        and (
            swap_out.contract_address == swap_in.from_address
            or swap_out.to_address == swap_in.contract_address
            or swap_out.to_address == swap_in.from_address
        )
        and _equal_within_percent(
            swap_out.token_out_amount,
            swap_in.token_in_amount,
            TOKEN_AMOUNT_THRESHOLD_PERCENT,
        )
    )

def _equal_within_percent(
        first_value: int, second_value: int, threshold_percent: float
    ) -> bool:
        difference = abs(
            (first_value - second_value) / (0.5 * (first_value + second_value))
        )
        return difference < threshold_percent
