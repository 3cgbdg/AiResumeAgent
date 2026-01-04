from langchain_openai import OpenAI

llm = OpenAI(
    model="gpt-4o-mini",
    temperature=0.4
)