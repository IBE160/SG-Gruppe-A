# Backend

## How to Run

To run the server locally using `uv`, navigate to the `backend` directory and run:

```bash
uv run uvicorn main:app --port 8000
```

For development with hot-reloading:

```bash
uv run uvicorn main:app --port 8000 --reload
```