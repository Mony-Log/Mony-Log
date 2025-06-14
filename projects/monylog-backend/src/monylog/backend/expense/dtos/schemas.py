from datetime import datetime
from decimal import Decimal
from monylog.shared_kernel.infra.camel_model import CamelModel, Field
from monylog.backend.llm.service.v1.schema import LangchainLLMExpenseAnalyzeResult
from monylog.shared_kernel.domain.enum import ExpenseType


class MessageAnalyzedSchema(LangchainLLMExpenseAnalyzeResult, CamelModel):
    pass


class ExpenseTagSchema(CamelModel):
    id: str
    name: str
    data: dict = Field(default_factory=dict)


class ExpenseSchema(CamelModel):
    title: str
    tags: list[str] = Field(default_factory=list)
    amount: Decimal = Field(default=Decimal("0.00"))
    dt: datetime
    type: ExpenseType = Field(default=ExpenseType.EXPENSE)


class ExpenseReadSchema(ExpenseSchema):
    id: int
    data: dict = Field(default_factory=dict)
    tags: list[ExpenseTagSchema] = Field(default_factory=list)
