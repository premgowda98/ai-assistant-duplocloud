from service.rag.train import VectorStore
from service.workflow import Chat


def chat_with_llm(model_type: str, embedding_type: str, query: str):
    vs = VectorStore(embedding_type)
    vs.load_store()

    llm = Chat(model_type)
    llm.setup_rag_tool(vs.retriever)

    return llm.query(query)
