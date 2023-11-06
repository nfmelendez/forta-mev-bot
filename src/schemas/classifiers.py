from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from .liquidations import Liquidation
from .swaps import Swap
from .events import Classification, Protocol, DecodedEvent, ClassifiedEvent
from .transfers import Transfer
from .flashloan import FlashLoan


class Classifier(ABC):
    @staticmethod
    @abstractmethod
    def get_classification() -> Classification:
        raise NotImplementedError()


class TransferClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.transfer

    @staticmethod
    @abstractmethod
    def get_transfer(event: DecodedEvent) -> Transfer:
        raise NotImplementedError()


class SwapClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.swap

    @staticmethod
    @abstractmethod
    def parse_swap(
        event: DecodedEvent,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:
        raise NotImplementedError()


class LiquidationClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.liquidate

    @staticmethod
    @abstractmethod
    def parse_liquidation(
        liquidation_event: DecodedEvent,
        transfer_events: List[ClassifiedEvent]
    ) -> Optional[Liquidation]:
        raise NotImplementedError()

class FlashLoanClassifier(Classifier):
    @staticmethod
    def get_classification() -> Classification:
        return Classification.flashloan

    @staticmethod
    @abstractmethod
    def parse_flashloan(
        flahloan: DecodedEvent,
    ) -> Optional[FlashLoan]:
        raise NotImplementedError()



class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifiers: Dict[str, Type[Classifier]] = {}
