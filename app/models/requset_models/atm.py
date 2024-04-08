from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, validator, root_validator, Field

MAX_DECIMAL_PLACES = 2

MAX_WITHDRAWAL_AMOUNT = 2000
VALID_WITHDRAWAL_FIELDS = ('0.01', '0.1', '1', '5', '10', '20', '100', '200')


class InputValueError(ValueError):
    pass


class NotValidFieldError(ValueError):
    pass


class ReqWithdrawal(BaseModel):
    amount: float

    @validator('amount')
    def name_must_contain_space(cls, v):
        if v is None or v <= 0:
            raise InputValueError(f'Amount must be number or float greater than 0, but got {v} instead.')
        number_of_decimal_places = abs(Decimal(str(v)).as_tuple().exponent)
        if number_of_decimal_places > MAX_DECIMAL_PLACES:
            raise InputValueError(f'Max decimal places for amount is {MAX_DECIMAL_PLACES} '
                                  f'but got {number_of_decimal_places} instead.')
        if v > MAX_WITHDRAWAL_AMOUNT:
            raise InputValueError(f'Max amount to withdraw is {MAX_WITHDRAWAL_AMOUNT} but got {v} instead.')

        return v


# todo-sarel handle missing fields
class Denomination(BaseModel):
    cent: Optional[float] = Field(gt=0, alias="0.01", default=None)
    ten_cent: Optional[float] = Field(gt=0, alias="0.1", default=None)
    dollar: Optional[float] = Field(gt=0, alias="1", default=None)
    five_dollar: Optional[float] = Field(gt=0, alias="5", default=None)
    ten_dollar: Optional[float] = Field(gt=0, alias="10", default=None)
    twenty_dollar: Optional[float] = Field(gt=0, alias="20", default=None)
    hundred_dollar: Optional[float] = Field(gt=0, alias="100", default=None)
    tow_hundred_dollar: Optional[float] = Field(gt=0, alias="200", default=None)

    @root_validator(pre=True)
    def extract_features(cls, v):
        for field, value in v.items():
            if field not in VALID_WITHDRAWAL_FIELDS:
                raise NotValidFieldError(f'Expecting one of those fields: {VALID_WITHDRAWAL_FIELDS} but got {field}')
        return v


class ReqRefill(BaseModel):
    money: Denomination
