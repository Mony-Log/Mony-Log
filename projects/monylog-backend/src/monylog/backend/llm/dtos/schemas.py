from monylog.shared_kernel.infra.camel_model import CamelModel, Field
from monylog.backend.llm.service.v1.schema import ExpenseResult
from pydantic import computed_field


class MessageAnalyzedSchema(CamelModel):
    id: str
    expenses: list[ExpenseResult] = Field(default_factory=list)

    @computed_field
    @property
    def count(self) -> int:
        return len(self.expenses)


class ExpenseTagSchema(CamelModel):
    id: str
    name: str
    data: dict = Field(default_factory=dict)
