## Requirements

- VS Code
- Ollama
    - Working Ollama model
- Python (ideally 3.14.4)
- Recommended Python extensios


## Setup

```sh
git clone git@github.com:davidneuhaeuser/ollama_indexer.git
cd ollama_indexer
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Running

```sh
# with activated venv
python ./src/search_engine.py
```

## Testing

### High-level Testing of Indexing and LLM

Simply ask questions that the LLM *should* be able to answer.

## Contributing - Goals

- Well working system prompt
- Well working indexing duh