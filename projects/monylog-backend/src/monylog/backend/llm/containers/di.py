from dependency_injector import containers, providers

# from ..use_case import ExpenseUseCase
from monylog.backend.llm.service.v1 import LangchainLLMExpenseAnalyzer
from monylog.backend.settings import Settings
from ..use_case.expense_use_case import ExpenseLLMUseCase


class LLMContainer(containers.DeclarativeContainer):
    settings = providers.Resource(Settings)
    analyzer = providers.Singleton(LangchainLLMExpenseAnalyzer, config=settings.provided.expense_analyzer)
    use_case = providers.Dict(expense=providers.Singleton(ExpenseLLMUseCase, analyzer=analyzer))
