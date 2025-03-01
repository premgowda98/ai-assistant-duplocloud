# AI Agentic Chatbot

Chatbot has the following features:

1. Ability to load documents from GitHub repositories and train the RAG model.
2. Search YouTube videos by person or event, providing the latest videos.
3. Search the internet for the latest events and help users with their questions.
4. Supports OpenAI and Google AI models, as well as embedding models.

## Tech Stack

1. **LLM Framework**: Langchain
2. **UI**: Streamlit
3. **Backend API**: FastAPI
4. **Containerization**: Docker
5. **LLM Models**: OpenAI, Gemini

## How to Run

### Access the Hosted Version

1. UI: [https://ui-chatbot.premgowda.in](https://ui-chatbot.premgowda.in)
2. API: [https://api-chatbot.premgowda.in/docs](https://api-chatbot.premgowda.in/docs)

### Run as Docker

1. Ensure Docker is installed on your system.
2. If running on Linux, use the following commands:
    - `make docker_build` to build the image.
    - `make docker_run` to run the containers.
3. If the `Make` command is not available:
    1. Run `docker build -t localhost:5000/duplocloud-ai-assistant:latest docker/Dockerfile` to build the image.
    2. To run the container, use the command: `docker compose -f docker/docker-compose.yml up -d`.

### Run as a Process

1. Create a virtual environment using the command: `python -m venv .venv` and activate it using: `source .venv/bin/activate`.
2. Install dependencies: `pip install -r requirements.txt`.
3. To run the application: `python src/main.py`.

### Access the Application

1. UI can be accessed at: [http://localhost:8501](http://localhost:8501).
2. Backend API can be accessed at: [http://localhost:8005/docs](http://localhost:8005/docs).

### Note

- The `.env` file must be present in the root directory. You can find the format in the `.env.tmpl` file.

## How to Test the Application

1. Select the appropriate LLM model and embedding model on the UI.
2. Input the GitHub repository URL.
3. Click on the **Train** button to start the training.
4. In the chat interface, the following questions can be asked:
    1. **What are the 3 main diagnostic functions of the Duplocloud platform?**
        - This will be answered based on the RAG model.
    2. **Give me 3 videos of Steve Jobs.**
        - For this question, the agent will use the YouTube search tool to provide the response.
    3. **Give me some information regarding the 2025 Champions Trophy.**
        - For this, the agent uses the Travily search tool to get the latest updates from the internet.

## Scope of Improvement

1. Provide citation sources for the given response.
2. Increase GitHub functionality to report on issues, pull requests (PRs), etc.