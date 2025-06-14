from fastapi import APIRouter
from monylog.backend.expense.rest.fastapi import router as expense_router
from monylog.backend.llm.rest.fastapi import router as llm_router
endpoint = APIRouter(prefix="/api")

endpoint.include_router(expense_router)
endpoint.include_router(llm_router)
