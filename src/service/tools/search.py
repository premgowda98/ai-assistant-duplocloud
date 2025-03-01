from langchain_core.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Type
from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class SearchInput(BaseModel):
    query: str = Field("search input")

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "this toll helps in searching the internet for the latest information"
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        results = tavily_client.search(query)

        return f"Search results for query: {query}\n\n results:{results}"
