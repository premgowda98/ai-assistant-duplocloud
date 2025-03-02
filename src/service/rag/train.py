import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders.github import GithubFileLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

import constants.embeddings as embd_const
import constants.store as store_const
from utils.errors import VectorStoreNotLoadedError


class VectorStore:
    def __init__(self, embedding_type: str):
        self.embedding_model = self._select_embedding_model(embedding_type)
        self.embedding_type = embedding_type
        self.retriever = None

    def _select_embedding_model(self, embedding_type: str):
        if embedding_type in embd_const.GOOGLE_EMBEDDING_MODELS:
            return GoogleGenerativeAIEmbeddings(model=embedding_type)
        if embedding_type in embd_const.OPENAI_EMBEDDING_MODELS:
            return OpenAIEmbeddings(model=embedding_type)

        self.embedding_type = embd_const.GOOGLE_EMBEDDING_004
        return GoogleGenerativeAIEmbeddings(model=embd_const.GOOGLE_EMBEDDING_004)

    def train(self, loader=Literal[GithubFileLoader]) -> bool:
        try:
            documents = loader.load()

            # Split the documents
            text_spliter = CharacterTextSplitter(chunk_size=512, chunk_overlap=30)
            docs = text_spliter.split_documents(documents)

            # create vector store
            Chroma.from_documents(
                docs, self.embedding_model, persist_directory=store_const.PERSISTENT_DIR
            )

            self._save_training_info()

            self.load_store()

            return True
        except Exception as e:
            print(e)
            return False

    def _save_training_info(self):
        training_metadata = {
            "embedding_model": self.embedding_type,
            "trained_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "persistent_dir": store_const.PERSISTENT_DIR,
        }

        with open(f"{store_const.PERSISTENT_DIR}/metdata.json", "w") as file:
            file.write(json.dumps(training_metadata))

    def _load_training_info(self):
        with open(f"{store_const.PERSISTENT_DIR}/metdata.json", "r") as file:
            return json.loads(file.read())

    def load_store(self):
        if not Path(store_const.PERSISTENT_DIR).exists():
            raise FileNotFoundError("db not found, the model has not been trained")

        metadata = self._load_training_info()

        db = Chroma(
            persist_directory=metadata["persistent_dir"],
            embedding_function=self._select_embedding_model(
                metadata["embedding_model"]
            ),
        )

        self.retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 9, "score_threshold": 0.4},
        )

        return True

    def query(self, q: str):
        if not self.retriever:
            raise VectorStoreNotLoadedError("vector store not loaded")

        return self.retriever.invoke(q)
