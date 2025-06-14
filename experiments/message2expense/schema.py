from datetime import date
from decimal import Decimal

from pendulum import DateTime
from pydantic import BaseModel, Field, computed_field, SecretStr

from enum import StrEnum  # noqa: F401


class ExpenseType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class Gender(StrEnum):
    M = "M"
    F = "F"


class ApplicationMode(StrEnum):
    devel = "DEV"
    production = "PROD"
    admin = "ADMIN"
    test = "test"


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
    expenses: list[ExpenseResult] = Field(description="The result of the expenses extraction from the user message.")

    @computed_field
    @property
    def count(self) -> int:
        return len(self.expenses)


class LangchainLLMExpenseAnalyzeResult(BaseModel):
    id: str = Field(
        description="The unique identifier for the expense analysis result.",
    )
    message: str = Field(
        description="The original user message that was analyzed for expenses.",
    )
    expenses: list[ExpenseResult] = Field(
        default_factory=list,
        description="The result of the expenses extraction from the user message.",
    )


class LangchainLLMExpenseAnalyzerConfig(BaseModel):
    base_url: str = Field(default="http://192.168.81.2:11434/v1")
    api_key: SecretStr = Field(default=SecretStr("ollama"))
    model: str = Field(default="")
    temperature: float = Field(default=0.0)
    max_tokens: int = Field(default=10240)
