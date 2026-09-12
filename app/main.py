from fastapi import FastAPI
from api.v1.users.router import users_router
from api.v1.transactions.router import transactions_router
from api.v1.payments.router import payments_router
app = FastAPI()


app.include_router(users_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")
app.include_router(payments_router,prefix="/api/v1")