from monylog.shared_kernel.infra.camel_model import CamelModel, Field
from pydantic import model_validator


class ExpenseMessageAnalyzeRequest(CamelModel):
    message: str
    tags: list[str] = Field(
        default_factory=list,
    )

    @model_validator(mode="after")
    def validate_at_tags_count(self) -> "ExpenseMessageAnalyzeRequest":
        if len(self.tags) == 0:
            raise ValueError("tags must be need!")
        return self
