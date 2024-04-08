import sqlite3
from contextlib import contextmanager

from common.const import AMOUNT, VALUE

DELETE_FROM_BALANCE = "DELETE FROM balance"

DB_CONNECTIO_PATH = "./db/ATM.db"
TYPE = "Type"

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {type} TEXT NOT NULL,
        {value} REAL UNIQUE NOT NULL  ,
        {amount} INTEGER NOT NULL)
    """.format(amount=AMOUNT,
               value=VALUE,
               type=TYPE)

INSERT_QUERY = """
    INSERT OR IGNORE INTO balance ({type}, {value}, {amount}) 
        VALUES ('BILL', 200, 1), ('BILL', 100, 2), ('BILL', 20, 5), ('COIN', 10, 10),
            ('COIN', 1, 10), ('COIN', 5, 10), ('COIN', 0.1, 1), ('COIN', 0.01, 10)
            """.format(amount=AMOUNT,
                       value=VALUE,
                       type=TYPE)


@contextmanager
def get_db_connection():
    connection = sqlite3.connect(DB_CONNECTIO_PATH)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def execute_query(query: str):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)


def fetchall_query(query: str):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        return cursor.execute(query).fetchall()


def initial_balance_table() -> None:
    execute_query(query=CREATE_TABLE_QUERY)
    execute_query(query=DELETE_FROM_BALANCE)
    execute_query(query=INSERT_QUERY)
