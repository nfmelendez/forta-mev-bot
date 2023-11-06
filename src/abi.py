import json
from pathlib import Path
from typing import Optional

from pydantic import parse_obj_as



try:
    from src.schemas.abi import ABI
    from src.schemas.events import Protocol
except ModuleNotFoundError:
    from schemas.abi import ABI
    from schemas.events import Protocol


THIS_FILE_DIRECTORY = Path(__file__).parents[0]
ABI_DIRECTORY_PATH = THIS_FILE_DIRECTORY / "abis"


def get_abi_path(abi_name: str, protocol: Optional[Protocol]) -> Optional[Path]:
    abi_filename = f"{abi_name}.json"
    abi_path = (
        ABI_DIRECTORY_PATH / abi_filename
        if protocol is None
        else ABI_DIRECTORY_PATH / protocol.value / abi_filename
    )
    if abi_path.is_file():
        return abi_path

    return None


def get_raw_abi(abi_name: str, protocol: Optional[Protocol]) -> Optional[str]:
    abi_path = get_abi_path(abi_name, protocol)
    if abi_path is not None:
        with abi_path.open() as abi_file:
            return abi_file.read()

    return None


def get_abi(abi_name: str, protocol: Optional[Protocol]) -> Optional[ABI]:
    abi_path = get_abi_path(abi_name, protocol)
    if abi_path is not None:
        with abi_path.open() as abi_file:
            abi_json = json.load(abi_file)
            return parse_obj_as(ABI, abi_json)

    return None
