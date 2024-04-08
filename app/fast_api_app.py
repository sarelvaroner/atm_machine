from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY

from common.threads_management import lock
from db.db import initial_balance_table
from logic.withdrawal import NotEnoughBalance, ToMuchCoinsError
from routes.atm import router as atm_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    with lock:
        initial_balance_table()


@app.exception_handler(NotEnoughBalance)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(exc))


@app.exception_handler(ToMuchCoinsError)
async def validation_exception_handler(request, exc):
    raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


app.include_router(atm_router)
