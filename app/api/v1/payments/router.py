from fastapi import APIRouter

payments_router = APIRouter(prefix="payments",
                            tags=["Payments"]
                            )
