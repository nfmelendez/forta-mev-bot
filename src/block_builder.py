try:
    from src.schemas.block_builder import BlockBuilder
except ModuleNotFoundError:
    from schemas.block_builder import BlockBuilder


BLOCK_BUILDERS = [
    BlockBuilder(name="Flashbots",addresses=[
        "0x5a0b54d5dc17e0aadc383d2db43b0a0d3e029c4c".lower(), 
        "0xdafea492d9c6733ae3d56b7ed1adb60692c98bc5".lower()
        ], chain_id=1),

    BlockBuilder(name="Titan Builder",addresses=[
        "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97".lower()
        ], chain_id=1),

    BlockBuilder(name="rsync-builder",addresses=[
        "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97".lower()
        ], chain_id=1),
    BlockBuilder(name="beaverbuild",addresses=[
        "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5".lower()
        ], chain_id=1),

    BlockBuilder(name="builder0x69",addresses=[
        "0x690B9A9E9aa1C9dB991C7721a92d351Db4FaC990".lower()
        ], chain_id=1),      
]


def get_block_builder(address:str, chain_id:int) -> BlockBuilder:
    for bb in  BLOCK_BUILDERS:
        if bb.chain_id == chain_id:
            if address.lower() in bb.addresses:
                return bb
    return None



