from service.rag.loader import GithubLoader
from service.rag.train import VectorStore

def train_model(url: str, model: str, embedding:str):
    github = GithubLoader(url=url)
    loader = github.load()

    vs = VectorStore(embedding)
    vs.train(loader=loader)

    return True

def query_vector_store(query: str, embedding: str):
    vs = VectorStore(embedding)
    vs.load_store()
    return vs.query(query)

