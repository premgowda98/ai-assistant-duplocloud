from typing import Literal

from pydantic import BaseModel, Field

import constants.embeddings as embd_const
import constants.models as models_const


class ModelMetadata(BaseModel):
    llm_type: str = Field(
        default=models_const.GOOGLE_15_PRO,
        description="Choose the appropriate llm model",
    )
    embedding_type: str = Field(
        default=embd_const.GOOGLE_EMBEDDING_004,
        description="Choose the appropriate embedding",
    )


class TrainingMetadata(ModelMetadata):
    url: str = Field(
        default="https://github.com/duplocloud/docs/tree/main/getting-started-1",
        description="The github url on which rag model has to be trained",
    )


class ChatQuery(BaseModel):
    q: str = Field()
    llm_type: Literal[*models_const.ALL_MODELS] = models_const.GOOGLE_15_PRO  # type: ignore
    embedding_type: Literal[*embd_const.ALL_EMBEDDINGS] = (  # type: ignore
        embd_const.GOOGLE_EMBEDDING_004
    )


ModelDescription = "**Supported LLM Models**\n\n"

for ind, model in enumerate(models_const.ALL_MODELS):
    ModelDescription += f"\t{ind + 1}. {model}\n"

EmbeddingDescription = "**Supported Embedding Models**\n\n"

for ind, model in enumerate(embd_const.ALL_EMBEDDINGS):
    EmbeddingDescription += f"\t{ind + 1}. {model}\n"

AppDescription = """
### DuploCloud AI Assistant API\n\n

This API provides access to an AI-powered assistant that can answer questions about 
DuploCloud by retrieving information from documentation and searching the internet when needed.\n\n

#### Features:\n
- Retrieval-Augmented Generation (RAG) for accurate answers from DuploCloud documentation loaded directly from GitHub\n
- Internet search capability powered by Travily for answering general knowledge questions\n
- YouTube video search tool that provides relevant video resources on requested topics or people\n
- Query routing between documentation, web search, and video resources\n\n

The assistant is designed to provide helpful, accurate responses to both technical questions about DuploCloud's application-focused interface and general knowledge queries by 
leveraging:\n
1. A knowledge base built from DuploCloud's GitHub documentation repository\n
2. Real-time web search capabilities via Travily for up-to-date information\n
3. YouTube video search for visual learning resources and tutorials\n
4. LLM integration for natural language understanding and context-aware responses\n"""
