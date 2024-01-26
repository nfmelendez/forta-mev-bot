from typing import Dict, Optional, Tuple, Type

try:
    from src.schemas.classifiers import Classifier, ClassifierSpec
    from src.schemas.events import Protocol, DecodedEvent
except ModuleNotFoundError:
    from schemas.classifiers import Classifier, ClassifierSpec
    from schemas.events import Protocol, DecodedEvent

from .aave import AAVE_CLASSIFIER_SPECS
from .erc20 import ERC20_CLASSIFIER_SPECS
from .uniswap import UNISWAP_CLASSIFIER_SPECS
from .balancer import BALANCER_CLASSIFIER_SPECS
from .paraswap import PARASWAP_CLASSIFIER_SPECS
from .zero_ex import ZEROEX_CLASSIFIER_SPECS
from .dxdy import DXDY_CLASSIFIER_SPECS
from .one_inch import ONEINCH_CLASSIFIER_SPECS
from .bancor import BANCOR_CLASSIFIER_SPECS
from .weth import WETH_CLASSIFIER_SPECS
from .curvefi import CURVEFI_CLASSIFIER_SPECS

ALL_CLASSIFIER_SPECS = (
    DXDY_CLASSIFIER_SPECS +
    ZEROEX_CLASSIFIER_SPECS +
    ERC20_CLASSIFIER_SPECS
    + UNISWAP_CLASSIFIER_SPECS
    + AAVE_CLASSIFIER_SPECS
    + BALANCER_CLASSIFIER_SPECS
    + PARASWAP_CLASSIFIER_SPECS
    + ONEINCH_CLASSIFIER_SPECS
    + BANCOR_CLASSIFIER_SPECS
    + WETH_CLASSIFIER_SPECS
    + CURVEFI_CLASSIFIER_SPECS
    
)

_SPECS_BY_ABI_NAME_AND_PROTOCOL: Dict[
    Tuple[str, Optional[Protocol]], ClassifierSpec
] = {(spec.abi_name, spec.protocol): spec for spec in ALL_CLASSIFIER_SPECS}


def get_classifier(
    event: DecodedEvent,
) -> Optional[Type[Classifier]]:
    abi_name_and_protocol = (event.abi_name, event.protocol)
    spec = _SPECS_BY_ABI_NAME_AND_PROTOCOL.get(abi_name_and_protocol)

    if spec is not None:
        return spec.classifiers.get(event.event_signature)

    return None
