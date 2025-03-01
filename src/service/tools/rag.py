from langchain import chains
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain

class RAGChain:
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store
        self._set_context()
        self._enable_history()
        self._set_system_prompt()

    def _set_context(self):
        contextualized_system_prompt = (
            "Given a chat history and the latest user question which might reference context in chat history"
            "formulate a standalone question which can be understood without chat history"
            "DO NOT answer the question, just reformulate it if needed and otherwise return it as is"
        )

        self.context_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualized_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ]
        )

    def _enable_history(self):
        self.history_aware_retriever = chains.create_history_aware_retriever(
            self.llm, self.vector_store, self.context_prompt
        )

    def _set_system_prompt(self):
        qa_system_prompt = (
            "You are an AI Assistant for question answering tasks"
            "Use the following retrieved context to answer the question."
            "If you don't know the answer, just say you don't know. Use 3 sentence max and keep answer short"
            "\n\n"
            "{context}"
        )

        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

    def get_chain(self):

        question_answer_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
        rag_chain = chains.create_retrieval_chain(self.history_aware_retriever, question_answer_chain)

        return rag_chain



