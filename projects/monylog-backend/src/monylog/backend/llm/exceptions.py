from monylog.shared_kernel.infra.fastapi.exception_handlers.base import BaseMsgException


class LLMException(BaseMsgException):
    """
    Base exception for all expense-related errors.
    """

    error: str = ""
    message: str = ""
    code: int = 500


class ExpenseNotAnalyzedException(LLMException):
    """
    Exception raised when an expense has not been analyzed.
    """

    error: str = "ExpenseNotAnalyzed"
    message = "analyzed expense count is 0, please analyze new message."
    code: int = 404
