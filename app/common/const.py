from dataclasses import dataclass

COIN = "COIN"
AMOUNT = "Amount"
VALUE = "Value"


@dataclass
class Denomination:
    type: str
    value: float
    quantity: int


@dataclass
class DenominationUpdates:
    value: str
    quantity: float


