# AI Agentic Chatbot

This project follows a modular architecture to keep different concerns separated, allowing for better maintainability. The various components of the system are organized into distinct modules that each handle a specific responsibility. These modules can interact with each other making the system extensible and flexible.

## Features

1. Ability to load documents from GitHub repositories and train the RAG model.
2. Search YouTube videos by person or event, providing the latest videos.
3. Search the internet for the latest events and help users with their questions.
4. Supports OpenAI and Google AI models, as well as embedding models.

## Project Structure

The project has been organized into the following modular structure:

- **`src/api`**: This module handles the core API functionality with FastAPI. It includes route definitions, request/response schemas, and related business logic.
- **`src/constants`**: Contains constant values and configuration files used across different modules. This includes models, embeddings, and utility files.
- **`src/db`**: Contains the Vector Embeddings of a RAG Model.
- **`src/service`**: This module contains core business logic and services:
    - **`rag`**: Handles the RAG (retrieval-augmented generation) logic, including training and loading models.
    - **`tools`**: Contains specialized tools for functionalities like mathematical operations, RAG-based document retrieval, and external search operations.
    - **`workflow.py`**: Coordinates the entire workflow, ensuring that each service is called in the correct sequence for seamless operation.
- **`src/ui`**: Contains the Streamlit-based user interface (UI) and related modules for managing interactions on the front-end. Includes chat and training functionalities.
- **`src/utils`**: Provides utility functions, error handling, and validation logic that can be reused across the application to reduce code duplication.

This modular approach ensures that components are loosely coupled and focused on specific tasks. Each module can be independently developed, tested, and deployed.

## Tech Stack

1. **LLM Framework**: Langchain
2. **UI**: Streamlit
3. **Backend API**: FastAPI
4. **Containerization**: Docker
5. **LLM Models**: OpenAI, Gemini

## How to Run

### Access the Hosted Version

>Note: The app is hosted in my home server, hence it is uptime could be around 50-60%

1. UI: [https://ui-chatbot.premgowda.in](https://ui-chatbot.premgowda.in)
2. API: [https://api-chatbot.premgowda.in/docs](https://api-chatbot.premgowda.in/docs)

### Steps to run application locally 

>Note: The **.env** file must be present in the root directory. You can find the format in the **.env.tmpl** file.

### Run as Docker

1. Ensure Docker is installed on your system.
2. If running on Linux, use the following commands:
    - `make docker_build` to build the image.
    - `make docker_run` to run the containers.
3. If the **Make** command is not available:
    1. Run following command to build the image. 
    ```bash
    docker build -t localhost:5000/duplocloud-ai-assistant:latest docker/Dockerfile
    ```
    2. To run the container, use the command 
    ```bash 
    docker compose -f docker/docker-compose.yml up -d
    ```

### Run as a Process

1. Create a virtual environment using the command and activate it using
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies: 
```bash 
pip install -r requirements.txt
```
3. To run the application
```bash
python src/main.py
```

### Access the Application

1. UI can be accessed at: [http://localhost:8501](http://localhost:8501).
2. Backend API can be accessed at: [http://localhost:8005/docs](http://localhost:8005/docs).

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