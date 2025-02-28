from typing import Literal
import constants.embeddings as embd_const
import constants.store as store_const
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

from pathlib import Path

from utils.errors import VectorStoreNotLoaded

class VectorStore:
    def __init__(self, embedding_type: str):
        self.embedding_model = self._select_embedding_model(embedding_type)
        self.retriever = None

    def _select_embedding_model(self, embedding_type: str):
        if embedding_type in embd_const.GOOGLE_EMBEDDING_MODELS:
            return GoogleGenerativeAIEmbeddings(model=embedding_type)
        elif embedding_type in embd_const.OPENAI_EMBEDDING_MODELS:
            return OpenAIEmbeddings(model=embedding_type)
        
        return GoogleGenerativeAIEmbeddings(model=embd_const.GOOGLE_EMBEDDING_004)


    def train(self, loader = Literal[GithubFileLoader, WebBaseLoader]) -> bool:
        try:
            documents = loader.load()

            # Split the documents
            text_spliter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
            docs = text_spliter.split_documents(documents)

            # create vector store
            Chroma.from_documents(docs, self.embedding_model, persist_directory=store_const.PERSISTENT_DIR)

            self.load_store()

            return True
        except Exception as e:
            print(e)
            return False

    def load_store(self):
        if not Path(store_const.PERSISTENT_DIR).exists():
            raise FileNotFoundError("db not found, the model has not been trained")
        
        db = Chroma(persist_directory=store_const.PERSISTENT_DIR, embedding_function=self.embedding_model)

        self.retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.4}
        )

        return True
    
    def query(self, q: str):
        if not self.retriever:
            raise VectorStoreNotLoaded("vector store not loaded")

        relevant_docs = self.retriever.invoke(q)

        return relevant_docs
    

