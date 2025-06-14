from pydantic import BaseModel, Field, SecretStr


class LangchainLLMExpenseAnalyzerConfig(BaseModel):
    base_url: str = Field(default="http://127.0.0.1:1234/v1")
    api_key: SecretStr | str = Field(default=SecretStr("password"))
    model: str = Field(default="qwen/qwen3-4b")
    temperature: float = Field(default=0.0)
    max_tokens: int = Field(default=1024 * 4)
