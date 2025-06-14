from dependency_injector import containers, providers

from monylog.backend.settings import Settings

from ..use_case import ExpenseUseCase


class ExpenseContainer(containers.DeclarativeContainer):
    settings = providers.Resource(Settings)
    use_case = providers.Singleton(ExpenseUseCase)
