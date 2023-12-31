# Contributing Guide

## One Time Set-Up

⛔️ Set-up instructions assume you are on Mac OS ⛔️

1. Clone this repository:
    ```
    git clone https://github.com/chrissyw247/tinygen
    ```

2. Navigate to the project directory and activate a virtual environment:
    ```bash
    cd tinygen
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and set the envvar `OPENAI_API_KEY` to your OpenAI API key
    ```bash
    touch .env
    echo 'OPENAI_API_KEY="<your-openai-api-key>"' >> .env # Replace <your-openai-api-key> with actual API key
    ```

## Local development

⛔️ Local development instructions assume you are on Mac OS ⛔️

### Run backend in CLI with live reload

1. Set envvars
    ```bash
    set -a; source .env; set +a;
    ```

2. Run server
    ```bash
    uvicorn server.main:app --reload
    ```

    This command will start the server at http://127.0.0.1:8000

### Run backend using Docker

1. Run server
    ```bash
    docker-compose up --build
    ```

    This command will start the server at http://127.0.0.1:8000

## Viewing UI

View the locally running UI at: http://127.0.0.1:8000.

## Querying API

### Query locally running backend

Example query:
```bash
curl \
    --location 'http://127.0.0.1:8000/generate' \
    --form 'repo_url="https://github.com/jayhack/llm.sh"' \
    --form 'prompt="add a check for which os type"'
```

### Query remote running backend
```bash
curl \
    --location 'https://tinygen-christinewang.b4a.run/generate' \
    --form 'repo_url="https://github.com/jayhack/llm.sh"' \
    --form 'prompt="add a check for which os type"'
```
