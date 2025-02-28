from typing import Literal
import constants.embeddings as embd_const
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

from pathlib import Path

from utils.errors import VectorStoreNotLoaded

# curr_dir = os.path.dirname(os.path.abspath(__file__))
# persistent_dir = os.path.join(curr_dir, "db", "github")

# loader = GithubFileLoader(access_token=os.getenv("GITHUB_TOKEN"),     
#                         github_api_url="https://api.github.com",
#                             file_filter=lambda file_path: 'getting-started-1/application-focussed-interface' in file_path,
#                             branch="main",repo="duplocloud/docs",
    
#     )

class VectorStore:
    def __init__(self, embedding_type: str = Literal[embd_const.EMBEDDING_MODELS]):
        self.embedding_model = self._select_embedding_model(embedding_type)
        self.retriever = None

    def _select_embedding_model(embedding_type: str):
        if embedding_type in embd_const.GOOGLE_EMBEDDING_MODELS:
            return GoogleGenerativeAIEmbeddings(model=embedding_type)
        elif embedding_type in embd_const.OPENAI_EMBEDDING_MODELS:
            return OpenAIEmbeddings(model=embedding_type)
        
        return GoogleGenerativeAIEmbeddings(model=embd_const.GOOGLE_EMBEDDING_004)


    def train(self, persist_directory: Path, loader = Literal[GithubFileLoader, WebBaseLoader]) -> bool:
        if persist_directory.exists():
            return True
        
        try:
            documents = loader.load()

            # Split the documents
            text_spliter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
            docs = text_spliter.split_documents(documents)

            # create vector store
            Chroma.from_documents(docs, self.embedding_model, persist_directory=persist_directory)

            return True
        except Exception as e:
            print(e)
            return False

    def load_store(self, persistent_dir: Path):
        if not persistent_dir.exists():
            raise FileNotFoundError("directory not found")
        
        db = Chroma(persist_directory=persistent_dir, embedding_function=self.embedding_model)

        self.retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.4}
        )

        return True
    
    def query(self, q: str):
        if not self.retriever:
            VectorStoreNotLoaded("vector store not loaded")

        relevant_docs = self.retriever.invoke(q)

        return relevant_docs
    

