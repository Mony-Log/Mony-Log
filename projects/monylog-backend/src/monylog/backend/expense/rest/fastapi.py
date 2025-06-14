from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, status

from monylog.backend.container import MonyLogContainer
from monylog.backend.expense.use_case import ExpenseUseCase
from monylog.shared_kernel.infra.fastapi.dtos.response import PaginationResponse

from ..dtos.request import CreateExpenseRequest, CreateExpenseTagRequest, ExpenseQeuryRequest, SearchExpenseTagRequest
from ..dtos.response import ExpensePagingResponse, ExpenseTagPagingResponse
from ..dtos.schemas import ExpenseTagSchema

router = APIRouter(prefix="/expense", tags=["Expense"])

get_exponse_use_case = Provide[MonyLogContainer.expense.use_case]


@router.get(
    "/tags",
    response_model=ExpenseTagPagingResponse,
)
@inject
async def get_tags(
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
):
    response = use_case.get_tags()
    return ExpenseTagPagingResponse(
        status=status.HTTP_200_OK,
        data=[ExpenseTagSchema.model_validate(tag) for tag in response],
        message="Expense tags retrieved successfully.",
    )


@router.post(
    "/tags",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_tags(
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
    payload: CreateExpenseTagRequest = Body(),
):
    use_case.append_tag(name=payload.name, color=payload.data.color)


@router.delete(
    "/tags",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_tags(
    *,
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
    query: SearchExpenseTagRequest = Query(),
):
    use_case.delete_tag(id=query.id, name=query.name)


@router.patch(
    "/tags/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def update_tags(
    *,
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
    id: str = Path(),
    payload: CreateExpenseTagRequest = Body(),
):
    use_case.update_tag(id=id, **payload.model_dump())


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_expense(
    *,
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
    payload: CreateExpenseRequest = Body(),
):
    use_case.create_expense(payload=payload)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ExpensePagingResponse,
)
@inject
async def get_expense(
    *,
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
    payload: ExpenseQeuryRequest = Query(),
):
    expense = use_case.get_expenses(payload=payload)
    return ExpensePagingResponse(
        status=status.HTTP_200_OK,
        data=PaginationResponse.build(expense, payload),
        message="Expenses retrieved successfully.",
    )


@router.post(
    "{id}/note",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def edit_expense_note(
    *,
    use_case: ExpenseUseCase = Depends(get_exponse_use_case),
    id: int = Path(..., description="ID of the expense to edit"),
    node: str = Body(..., embed=True),
):
   expense = use_case.edit_expense_node(id=id, note=node)
