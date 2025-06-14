import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from monylog.backend.llm.rest.fastapi import router
from monylog.backend.llm.dtos.request import ExpenseMessageAnalyzeRequest
from monylog.backend.llm.dtos.schemas import MessageAnalyzedSchema
import fastapi

# Python


app = fastapi.FastAPI()
app.include_router(router)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
@patch("monylog.backend.llm.rest.fastapi.ExpenseLLMUseCase")
@patch("monylog.backend.llm.rest.fastapi.Provide")
def test_analyze_message_success(mock_provide, mock_expense_use_case, client):
    # Arrange
    mock_use_case_instance = AsyncMock()
    mock_use_case_instance.generate_expense_from_message.return_value = {"field1": "value1", "field2": "value2"}
    # Provide returns a dict with "expense" key pointing to our mock
    mock_provide.return_value = {"expense": mock_use_case_instance}

    payload = {"message": "Sample expense message", "tags": ["food", "lunch"]}

    # Patch dependency injection
    app.dependency_overrides = {fastapi.Depends(lambda: mock_provide.return_value): mock_provide.return_value}

    # Act
    response = client.post("/llm/expense", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Expense analysis completed successfully."
    assert data["data"] == MessageAnalyzedSchema.model_validate({"field1": "value1", "field2": "value2"}).model_dump()
