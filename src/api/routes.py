import os, sys

# Get the parent directory of the working file/s
# Then append the parent directory to sys.path
parent_dir = os.path.dirname(os.path.abspath("src/"))
sys.path.append(parent_dir)
parent_dir = os.path.dirname(os.path.abspath("src/model/"))
sys.path.append(parent_dir)
parent_dir = os.path.dirname(os.path.abspath("src/api/"))
sys.path.append(parent_dir)

from langserve import CustomUserType, add_routes
from langchain.schema.runnable import RunnableLambda
from fastapi import FastAPI
from src.model.main import run_llm
from dotenv import load_dotenv
import uvicorn

load_dotenv()


api_app = FastAPI(
    title="iSAPedia",
    version="1.0",
    description="An API server to answers questions based on KB Articles.",
)


class TextRequest(CustomUserType):
    """Request body for text input, containing the question to ask the model."""

    question: str


def _process_request(request: TextRequest):
    response = run_llm(request.question)
    return response["result"]


add_routes(
    api_app,
    RunnableLambda(_process_request).with_types(input_type=TextRequest),
    config_keys=["configurable"],
    path="/api",
)

# if __name__ == "__main__":
#     uvicorn.run(api_app, host="localhost", port=8000)
