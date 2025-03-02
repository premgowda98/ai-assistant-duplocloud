from langchain import chains
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# https://dev.to/guilhermecxe/how-a-history-aware-retriever-works-5e07
# https://vijaykumarkartha.medium.com/beginners-guide-to-conversational-retrieval-chain-using-langchain-3ddf1357f371


class RAGChain:
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store

    def history_retriever(self):
        """
        This prompt helps is creating a search query based on the user input which is used to get documents from
        vector store.
        """

        retriever_prompt_context = (
            "Given a chat history and the latest user question which might reference context in chat history"
            "formulate a standalone question which can be understood without chat history"
            "DO NOT answer the question, just reformulate it if needed and otherwise return it as is"
        )

        retriever_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", retriever_prompt_context),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # https://api.python.langchain.com/en/latest/chains/langchain.chains.history_aware_retriever.create_history_aware_retriever.html#langchain.chains.history_aware_retriever.create_history_aware_retriever
        self.history_retriever_chain = chains.create_history_aware_retriever(
            self.llm, self.vector_store, retriever_prompt
        )

    def prompt_llm(self):
        """
        This prompt is used for the LLM along with the documents, chat_history and user input
        """
        qa_system_prompt = (
            "You are an AI Assistant for question answering tasks"
            "Use the following retrieved context to answer the question."
            "If you don't know the answer, just say you don't know, try to use other web search tools to gather more information."
            "\n\n"
            "{context}"
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self.document_chain = create_stuff_documents_chain(self.llm, qa_prompt)

    def retrieval_chain(self):
        """
        Here the retrieval chain is created using retriever_chain and
        document_chain to create conversational chain
        """

        self.history_retriever()
        self.prompt_llm()

        return chains.create_retrieval_chain(
            self.history_retriever_chain, self.document_chain
        )
