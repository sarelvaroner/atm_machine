from typing import Tuple, List

from common.const import Denomination, AMOUNT, VALUE, DenominationUpdates
from db.db import execute_query, fetchall_query

FILL_BALANCE_TABLE_QUERY = """
    UPDATE balance
          SET {amount} = CASE {value} 
                            {cases}
                         END              
    WHERE {value} IN ({rows_to_update});
"""

CASE_WHEN_STR = "WHEN {value} THEN {amount} + {quantity} \n"
GET_BALANCE_QUERY = """select * from balance"""


def update_balance(updates: List[DenominationUpdates]) -> None:
    _filtered_updates = [u for u in updates if u.quantity is not None]
    rows_to_update = ",".join([str(u.value) for u in _filtered_updates])
    cases = " ".join([CASE_WHEN_STR.format(value=u.value,
                                           quantity=u.quantity,
                                           amount=AMOUNT) for u in _filtered_updates])
    query = FILL_BALANCE_TABLE_QUERY.format(amount=AMOUNT,
                                            value=VALUE,
                                            cases=cases,
                                            rows_to_update=rows_to_update)
    execute_query(query)


def get_balance() -> Tuple[Denomination, ...]:
    result = fetchall_query(GET_BALANCE_QUERY)
    return tuple(Denomination(type=d[1],
                              value=d[2],
                              quantity=d[3]) for d in result)
