# My Tiny Gen

## Description

Baby gen!

## Installation

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

4. Set OPENAI_API_KEY envvar to your OpenAI API key

## Usage

1. Run server
    ```bash
    uvicorn server.main:app --reload
    ```

    This command will start the server at http://127.0.0.1:8000

2. Query server:
    Example query:
    ```
    curl \
        --location 'http://127.0.0.1:8000/generate' \
        --form 'repo_url="https://github.com/chrissyw247/tinygen"' \
        --form 'prompt="also print goodbye world"'
    ```