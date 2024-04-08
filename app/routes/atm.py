from fastapi import APIRouter

from common.const import DenominationUpdates, COIN
from common.threads_management import lock
from db.atm import get_balance, update_balance
from logic.withdrawal import calculate_withdrawal
from models.requset_models.atm import ReqWithdrawal, ReqRefill

SUCCESS = "success"
ATM = "atm"
COINS = "coins"
BILLS = "bills"
RESULT = "result"
MONEY = 'money'
BILL = "BILL"
ONE_CENT = "cent"
TEN_CENT = "ten_cent"
ONE_DOLLAR = "dollar"
FIVE = "five_dollar"
TEN = "ten_dollar"
TWENTY = "twenty_dollar"
ONE_HUNDRED = "hundred_dollar"
TWO_HUNDRED = "tow_hundred_dollar"
MAPPER = {
    TWO_HUNDRED: "200",
    ONE_HUNDRED: "100",
    TWENTY: "20",
    TEN: "10",
    FIVE: "5",
    ONE_DOLLAR: "1",
    TEN_CENT: "0.1",
    ONE_CENT: "0.01"
}

router = APIRouter(prefix=f"/{ATM}")


@router.post("/withdrawal", tags=[ATM])
async def withdrawal(req: ReqWithdrawal):
    with lock:
        balance = get_balance()
        withdrawal_denominations = calculate_withdrawal(amount=req.amount, balance=balance)
        update_balance(updates=withdrawal_denominations)
        denomination_types = {str(d.value): d.type for d in balance}
        return {
            RESULT: {
                BILLS: _filtered_denomination_by_type(denomination_types, withdrawal_denominations, BILL),
                COINS: _filtered_denomination_by_type(denomination_types, withdrawal_denominations, COIN)
            }
        }


def _filtered_denomination_by_type(denomination_types, withdrawal_denominations, denomination_type):
    return {i.value: abs(i.quantity) for i in withdrawal_denominations
            if denomination_types[i.value] == denomination_type}


@router.post("/refill", tags=[ATM])
async def refill(req: ReqRefill):
    with lock:
        update_balance(updates=[DenominationUpdates(value=MAPPER[k], quantity=v)
                                for k, v in req.dict()[MONEY].items() if v is not None])
        return SUCCESS
