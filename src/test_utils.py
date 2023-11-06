import json
import os
from typing import List
from pydantic import RootModel


try:
    from src.schemas.sandwiches import Sandwich
except ModuleNotFoundError:
    from schemas.sandwiches import Sandwich

Sandwiches = RootModel[List[Sandwich]]


THIS_FILE_DIRECTORY = os.path.dirname(__file__)
TEST_BLOCKS_DIRECTORY = os.path.join(THIS_FILE_DIRECTORY, "blocks")
TEST_SANDWICHES_DIRECTORY = os.path.join(THIS_FILE_DIRECTORY, "test/sandwiches")
TEST_ARBITRAGES_DIRECTORY = os.path.join(THIS_FILE_DIRECTORY, "test/arbitrages")
TEST_LIQUIDATION_DIRECTORY = os.path.join(THIS_FILE_DIRECTORY, "test/liquidations")




def load_test_sandwiches(block_number: int) -> List[Sandwich]:
    sandwiches_path = f"{TEST_SANDWICHES_DIRECTORY}/{block_number}.json"

    with open(sandwiches_path) as f:
        d = json.load(f)
        json_str = json.dumps(d)

        s = Sandwiches.model_validate_json(json_str)
        return s.root