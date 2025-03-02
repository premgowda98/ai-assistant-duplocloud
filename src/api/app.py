import uuid
from typing import Annotated

from fastapi import FastAPI, Path, Query, status
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse

import constants.embeddings as embd_const
import constants.models as models_const
from api.schemas import (
    AppDescription,
    ChatQuery,
    EmbeddingDescription,
    ModelDescription,
    TrainingMetadata,
)
from service.rag.loader import GithubLoader
from service.rag.train import VectorStore
from service.workflow import Chat
from utils.validations import validate_url

app = FastAPI(
    title="DuploCloud AI Assistant", description=AppDescription, version="1.0.0"
)

training_status = {}


def train_model(training_id: str, embedding_model: str, url: str):
    training_status[training_id] = False

    github = GithubLoader(url=url)
    loader = github.load()

    vs = VectorStore(embedding_model)
    vs.train(loader=loader)

    training_status[training_id] = True


def chat_with_llm(model_type: str, embedding_type: str, query: str):
    vs = VectorStore(embedding_type)
    vs.load_store()

    llm = Chat(model_type)
    llm.setup_rag_tool(vs.retriever)

    return llm.query(query)


@app.post("/train", description=ModelDescription + EmbeddingDescription)
def train(training_metadata: TrainingMetadata, background_task: BackgroundTasks):
    if training_metadata.llm_type not in models_const.ALL_MODELS:
        return JSONResponse(
            content={"message": "invalid llm", "data": {}, "error": ""},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if training_metadata.embedding_type not in embd_const.ALL_EMBEDDINGS:
        return JSONResponse(
            content={"message": "invalid embedding model", "data": {}, "error": ""},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not validate_url(training_metadata.url):
        return JSONResponse(
            content={"message": "invalid url", "data": {}, "error": ""},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    training_id = str(uuid.uuid4())
    training_status[training_id] = False
    background_task.add_task(
        train_model,
        training_id,
        training_metadata.embedding_type,
        training_metadata.url,
    )

    return JSONResponse(
        content={
            "message": "training started",
            "data": {"training_id": training_id, "status": "training"},
            "error": "",
        },
        status_code=status.HTTP_200_OK,
    )


@app.get("/train/{training_id}/status", description="Get the status of the training")
def get_training_status(training_id: str = Path()):
    if training_id not in training_status:
        return JSONResponse(
            content={"message": "training_id not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    status_message = (
        "training completed" if training_status[training_id] else "training ongoing"
    )

    return JSONResponse(
        content={
            "message": status_message,
            "data": {"training_id": training_id, "status": "trained"},
            "error": "",
        },
        status_code=status.HTTP_200_OK,
    )


@app.get("/chat")
def chat(
    query: Annotated[ChatQuery, Query(...)],
):
    if query.llm_type not in models_const.ALL_MODELS:
        return JSONResponse(
            content={"message": "invalid llm"}, status_code=status.HTTP_400_BAD_REQUEST
        )

    if query.embedding_type not in embd_const.ALL_EMBEDDINGS:
        return JSONResponse(
            content={"message": "invalid embedding model", "data": {}, "error": ""},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        response = chat_with_llm(query.llm_type, query.embedding_type, query.q)

        return JSONResponse(
            content={
                "message": "retrieved response",
                "data": {"response": response},
                "error": "",
            },
            status_code=status.HTTP_200_OK,
        )
    except FileNotFoundError:
        return JSONResponse(
            content={"message": "please train the model", "data": {}, "error": "model not trained"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JSONResponse(
            content={"message": "something went wrong", "data": {}, "error": e},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
