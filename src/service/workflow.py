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
from langchain_core.messages import SystemMessage
from service.tools.rag import RAGChain
from langchain.tools import Tool

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
initial_message = "You are AI Assistant that can provide helpful answers, using available tools"
memory.chat_memory.add_message(SystemMessage(initial_message))
    
class Chat:

    default_tools = [
        RandomNumberGeneratorTool(),
        YouTubeSearchTool(),
        WebSearchTool(),
    ]

    def __init__(self, model_type: str, tools: List = []):
        self.llm = self._select_model(model_type)
        self.tools = tools if tools else self.default_tools
        self.prompt = hub.pull("hwchase17/react")
        self.agent_executor = None
        self.rag_enabled = False

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
            memory=memory,
            handle_parsing_errors=True,
        )

        return agent_executor
    
    def setup_rag_tool(self, vector_store):

        rag = RAGChain(self.llm, vector_store)
        rag_chain = rag.get_chain()

        rag_tool = Tool(
            name="Answer Question - Duplocloud",
            func=lambda input, **kwargs: rag_chain.invoke(
                {"input": input, "chat_history": kwargs.get("chat_history", [])}
                ),
            description="Use when you need to answer questions about the duplocloud"
            )

        if not self.rag_enabled:
            self.rag_enabled = True
            self.tools.insert(0, rag_tool)
    
    def query(self, query: str):
        if not self.agent_executor:
            self.agent_executor = self._get_agent_executor()

        memory.chat_memory.add_user_message(query)
        response = self.agent_executor.invoke({"input": query})
        memory.chat_memory.add_ai_message(response["output"])

        return response["output"]
        
    
    





