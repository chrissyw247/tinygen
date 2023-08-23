# My Tiny Gen

## Description

Baby gen!

## One Time Set-Up

1. Clone this repository:
    ```
    git clone [repository-url]
    ```

2. Navigate to the project directory and activate a virtual environment:
    ```bash
    cd my-python-project
    python3 -m venv venv
    source venv/bin/activate # On Windows, use `.\myenv\Scripts\activate`
    ```

3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

## Local development

### Run backend in CLI

1. Set OPENAI_API_KEY envvar to your OpenAI API key

2. Run server
    ```bash
    uvicorn server.main:app --reload
    ```

    This command will start the server at http://127.0.0.1:8000

3. Query server:
    Example query:
    ```
    curl \
        --location 'http://127.0.0.1:8000/generate' \
        --form 'repo_url="https://github.com/chrissyw247/tinygen"' \
        --form 'prompt="I feel like the handling of the sys imports is weird? help clean it up?"'
    ```

### Run backend using Docker

1. Update `.env` file with your `OPENAI_API_KEY` key.

2. Build image
    ```bash
    docker build -t tinygen .
    ```

3. Run image
    ```bash
    docker run --env-file ./.env -p 8000:8000 tinygen
    ```

## Querying backend

### Query locally running backend

Example query:
```
curl \
    --location 'http://127.0.0.1:8000/generate' \
    --form 'repo_url="https://github.com/chrissyw247/tinygen"' \
    --form 'prompt="I feel like the handling of the sys imports is weird? help clean it up?"'
```

### Query remote running backend
```
curl \
    --location 'https://tinygen-christinewang.b4a.run/generate' \
    --form 'repo_url="https://github.com/chrissyw247/tinygen"' \
    --form 'prompt="I feel like the handling of the sys imports is weird? help clean it up?"'
```