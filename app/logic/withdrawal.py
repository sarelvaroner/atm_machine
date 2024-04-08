import logging
from decimal import Decimal
from typing import Tuple, List

from common.const import DenominationUpdates, Denomination, COIN
from db.atm import get_balance

MAX_CONES_PER_WITHDRAWAL = 50


class ToMuchCoinsError(ValueError):
    pass


class NotEnoughBalance(ValueError):
    pass


def calculate_withdrawal(amount: float, balance: Tuple[Denomination, ...]):
    _validate_enough_balance(amount, balance)

    current_balance = amount
    denomination_quantity_updates: List[DenominationUpdates] = []
    for d in _get_sorted_denominations(balance=balance):
        denomination_quantity_subtraction = get_denomination_quantity_subtraction(balance=current_balance,
                                                                                  denomination=d)
        if denomination_quantity_subtraction > 0:
            denomination_quantity_updates.append(DenominationUpdates(value=str(d.value),
                                                                     quantity=-denomination_quantity_subtraction))
        current_balance = current_balance - (d.value * denomination_quantity_subtraction)
    _validate_number_of_coins(denomination_quantity_updates)
    if abs(sum((float(d.value) * d.quantity) for d in denomination_quantity_updates)) != amount:
        _raise_not_enough_balance(amount, balance)
    return denomination_quantity_updates


def _validate_number_of_coins(denomination_quantity_updates: List[DenominationUpdates]):
    denomination_types = {str(d.value): d.type for d in get_balance()}
    number_of_coins = sum(d.quantity for d in denomination_quantity_updates if denomination_types[d.value] == COIN)
    if number_of_coins > MAX_CONES_PER_WITHDRAWAL:
        raise ToMuchCoinsError(f"Too much coins to withdrawal, "
                               f"the quantity of coins needed for this request is: {number_of_coins}, "
                               f"but the allowed max number of coins is {MAX_CONES_PER_WITHDRAWAL}.")


def _validate_enough_balance(amount: float, balance: Tuple[Denomination, ...]):
    if amount > sum(d.value for d in balance):
        _raise_not_enough_balance(amount, balance)


def get_denomination_quantity_subtraction(balance: float, denomination: Denomination) -> float:
    if denomination.quantity < 1 or denomination.value > balance:
        return 0.0
    return min(int(Decimal(str(balance)) // Decimal(str(denomination.value))), denomination.quantity)


def _get_sorted_denominations(balance: Tuple[Denomination, ...]) -> tuple[Denomination, ...]:
    available_denominations = (d for d in balance if d.quantity > 0)
    return tuple(sorted(available_denominations, key=lambda x: x.value, reverse=True))


def _raise_not_enough_balance(amount, balance):
    quantity_denomination = [f'quantity of {d.quantity} units for {d.value} denomination' for d in balance]
    msg = (f"""Not enough balance, the required amount is: {amount} """
           f"""and the quantities of denominations are: {', '.join(quantity_denomination)}.""")
    logging.error(msg)
    raise NotEnoughBalance(msg)
