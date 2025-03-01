from service.tools.math import RandomNumberGeneratorTool
from service.tools.search import WebSearchTool
from langchain_community.tools import YouTubeSearchTool
from langchain.agents import AgentExecutor, create_react_agent
import constants.models as models_const
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from typing import List
from langchain.memory import ConversationBufferMemory


class Chat:

    default_tools = [
        RandomNumberGeneratorTool(),
        YouTubeSearchTool(),
        WebSearchTool()
    ]

    def __init__(self, model_type: str, tools: List = []):
        self.llm = self._select_model(model_type)
        self.tools = tools if tools else self.default_tools
        self.prompt = hub.pull("hwchase17/react")
        self.agent_executor = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def _select_model(self, model_type: str):
        if model_type in models_const.GOOGLE_MODELS:
            return ChatGoogleGenerativeAI(model=model_type)
        elif model_type in models_const.OPENAI_MODELS:
            return ChatOpenAI(model=model_type)
        
        return ChatGoogleGenerativeAI(model=models_const.GOOGLE_15_FLASH)
    
    def _get_agent(self):
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            stop_sequence=True,
            )
        
        return agent
    
    def _get_agent_executor(self):
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self._get_agent(),
            tools=self.tools,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True,
        )

        return agent_executor
    
    def query(self, query: str):
        if not self.agent_executor:
            self.agent_executor = self._get_agent_executor()

        response = self.agent_executor.invoke({"input": query})

        return response["output"]
        
    
    





