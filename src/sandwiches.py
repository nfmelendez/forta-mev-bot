from typing import List, Optional

try:
    from src.schemas.sandwiches import Sandwich
    from src.schemas.swaps import Swap
    from src.config.routers import ROUTERS
except ModuleNotFoundError:
    from schemas.sandwiches import Sandwich
    from schemas.swaps import Swap
    from config.routers import ROUTERS

def get_sandwiches(chain_id, swaps: List[Swap]) -> List[Sandwich]:
    ordered_swaps = list(
        sorted(
            swaps,
            key=lambda swap: (swap.transaction_position, swap.log_index),
        )
    )

    sandwiches: List[Sandwich] = []

    for index, swap in enumerate(ordered_swaps):
        rest_swaps = ordered_swaps[index + 1 :]
        sandwich = _get_sandwich(chain_id, swap, rest_swaps)

        if sandwich is not None:
            sandwiches.append(sandwich)

    return sandwiches


def _get_sandwich(
    chain_id,
    front_swap: Swap,
    rest_swaps: List[Swap]
) -> Optional[Sandwich]:
    sandwicher_address = front_swap.to_address

    if chain_id in ROUTERS:
        if sandwicher_address in ROUTERS[chain_id]:
            return None

    sandwiched_swaps = []

    for other_swap in rest_swaps:
        if other_swap.transaction_hash == front_swap.transaction_hash:
            continue

        if other_swap.contract_address == front_swap.contract_address:
            if (
                other_swap.token_in_address == front_swap.token_in_address
                and other_swap.token_out_address == front_swap.token_out_address
                and other_swap.from_address != sandwicher_address
            ):
                sandwiched_swaps.append(other_swap)
            elif (
                other_swap.token_out_address == front_swap.token_in_address
                and other_swap.token_in_address == front_swap.token_out_address
                and other_swap.from_address == sandwicher_address
            ):
                if len(sandwiched_swaps) > 0:
                    return Sandwich(
                        block_number=front_swap.block_number,
                        sandwicher_address=sandwicher_address,
                        frontrun_swap=front_swap,
                        backrun_swap=other_swap,
                        sandwiched_swaps=sandwiched_swaps,
                        profit_token_address=front_swap.token_in_address,
                        profit_amount=other_swap.token_out_amount
                        - front_swap.token_in_amount,
                    )

    return None
