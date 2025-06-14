from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from langchain_openai import ChatOpenAI
from pendulum import DateTime

from .prompt import __PROMPT_TEMPLATE__
from .schema import LangchainLLMExpenseAnalyzeResult, ResultSchema
from .settings import LangchainLLMExpenseAnalyzerConfig

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableSerializable


@dataclass
class LangchainLLMExpenseAnalyzer:
    """
    A generic pipeline for analyzing expenses using Langchain LLM.
    This class is a placeholder for the actual implementation.
    """

    config: LangchainLLMExpenseAnalyzerConfig | dict = field(default_factory=LangchainLLMExpenseAnalyzerConfig)
    client: ChatOpenAI = field(init=False, repr=False)
    pipeline: "RunnableSerializable" = field(init=False, repr=False)

    def __post_init__(self):
        if isinstance(self.config, dict):
            self.config = LangchainLLMExpenseAnalyzerConfig(**self.config)
        self.client = ChatOpenAI(**self.config.model_dump())
        self.client = self.client.with_structured_output(schema=ResultSchema, include_raw=True, strict=True)  # type: ignore
        self.pipeline = __PROMPT_TEMPLATE__ | self.client | self.__output_processe

    def __output_processe(self, response: dict) -> LangchainLLMExpenseAnalyzeResult:
        return LangchainLLMExpenseAnalyzeResult(
            id=response["raw"].id,  # type: ignore
            message=response["raw"].content,  # type: ignore
            expenses=response["parsed"].expenses,  # type: ignore
        )

    async def aanalyze(
        self,
        message: str,
        tags: list[str],
        current_datetime: str = DateTime.now("Asia/Seoul").to_iso8601_string(),
        config: dict | None = None,
    ) -> LangchainLLMExpenseAnalyzeResult:
        response = await self.pipeline.ainvoke(
            dict(current_datetime=current_datetime, message=message, tags=tags),
            config=config,  # type: ignore
        )
        response.message = message.strip()
        return response

    def analyze(
        self,
        message: str,
        tags: list[str],
        current_datetime=DateTime.now("Asia/Seoul").to_iso8601_string(),
        config: dict | None = None,
    ) -> LangchainLLMExpenseAnalyzeResult:
        response = self.pipeline.invoke(
            dict(current_datetime=current_datetime, message=message, tags=tags),
            config=config,  # type: ignore
        )
        response.message = message.strip()
        return response
