from dataclasses import dataclass
from pendulum import DateTime

from monylog.shared_kernel.infra.database.sqla.mixin import SyncSqlaMixIn

from ..exceptions import ExpenseNotAnalyzedException
from ..service.v1 import LangchainLLMExpenseAnalyzer, LangchainLLMExpenseAnalyzeResult


@dataclass
class ExpenseLLMUseCase(SyncSqlaMixIn):
    analyzer: LangchainLLMExpenseAnalyzer

    async def generate_expense_from_message(
        self,
        message: str,
        tags: list[str],
        current_datetime: DateTime = DateTime.now("UTC"),
    ) -> LangchainLLMExpenseAnalyzeResult:
        result = await self.analyzer.aanalyze(message, tags, current_datetime.to_iso8601_string())
        if result.count == 0:
            raise ExpenseNotAnalyzedException
        return result
