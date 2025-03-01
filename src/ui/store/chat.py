from service.workflow import Chat
from service.rag.train import VectorStore

def chat_with_llm(model_type: str, embedding_type: str, query: str):
    vs = VectorStore(embedding_type)
    vs.load_store()
    
    llm = Chat(model_type)
    llm.setup_rag_tool(vs.retriever)

    print(llm.tools)

    response = llm.query(query)

    return response