from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


__SYSTEM_PROMPT = """
You are a helpful assistant that extracts expenses from user messages.
You will receive a user message and you need to extract the expenses from it.
The expenses can be of two types: income and expense.
You will return the expenses in a structured format.

ignore the not related sentences to the task, and extract the expenses and income from the user message.
The accuracy of the task is important. You must extract the expenses and income from the user message accurately.

You are an assistant specialized in extracting financial entries from free-form user messages.
Your job is to identify all expenses and incomes mentioned, determine their dates and amounts, and output them in a precise JSON format.
"""


__PROMPT_TEMPLATE__ = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(__SYSTEM_PROMPT),
        SystemMessagePromptTemplate.from_template("/no_think"),
        HumanMessagePromptTemplate.from_template("{message}"),
        HumanMessagePromptTemplate.from_template("current DATETIME with time zone is {current_datetime}"),
        HumanMessagePromptTemplate.from_template(
            """The following tags will be used as candidate labels during inference 
            candidate of tags is [{tags}]"""
        ),
    ]
)

__PROMPT_TEMPLATE_WITH_THINK__ = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(__SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{message}"),
        HumanMessagePromptTemplate.from_template("current DATETIME with time zone is {current_datetime}"),
        HumanMessagePromptTemplate.from_template(
            """The following tags will be used as candidate labels during inference 
            candidate of tags is [{tags}]"""
        ),
    ]
)
