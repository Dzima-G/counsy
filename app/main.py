from fastapi import FastAPI

app = FastAPI(title="counsy")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
