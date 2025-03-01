from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional
import random
from langchain.callbacks.manager import CallbackManagerForToolRun


class NumberRange(BaseModel):
    x: str = Field(description="first number")
    y: str = Field(description="second number")

class RandomNumberGeneratorTool(BaseTool):
    name: str = "random_number_generator_tool"
    description: str = "generates random number between the provided range"
    args_schema: Type[BaseModel] = NumberRange

    def _run(self, x: str, y: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool"""
        random_number = random.randint(int(x), int(y))

        return f"Random number between {x} and {y} is {random_number}"
