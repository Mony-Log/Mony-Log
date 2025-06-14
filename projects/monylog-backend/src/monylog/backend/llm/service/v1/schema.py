from datetime import date
from decimal import Decimal

from pendulum import DateTime
from pydantic import BaseModel, Field, computed_field

from monylog.shared_kernel.domain.enum import ExpenseType


class ExpenseResult(BaseModel):
    title: str = Field(
        description="The expense name from the user message.",
    )
    tags: list[str] = Field(
        description="The expense category tags from the message",
    )
    amount: Decimal = Field(
        default=Decimal("0.00"),
        description="The amount of the expense from the user message.",
    )
    dt: date = Field(
        default_factory=lambda: DateTime.now().date(),
        description="The date of the expense from the user message. defaults from the current date.",
    )

    type: ExpenseType = Field(
        description="The type of the expense, either income or expense.",
    )

    def __str__(self):
        return f"{self.type.value.capitalize()}-{self.title}-{self.amount}-[{self.tags}]"

    def __repr__(self):
        return self.__str__()


class ResultSchema(BaseModel):
    expenses: list[ExpenseResult] = Field(
        description="The result of the expenses extraction from the user message.",
    )

    @computed_field
    @property
    def count(self) -> int:
        return len(self.expenses)


class LangchainLLMExpenseAnalyzeResult(ResultSchema):
    id: str = Field(
        description="The unique identifier for the expense analysis result.",
    )
    message: str = Field(
        description="The original user message that was analyzed for expenses.",
    )
    tags: list[str] = Field(default_factory=list, description="candidate of tags")
