from fastapi import FastAPI

app = FastAPI(title="FedLedger")

@app.get("/health")
def health():
    return {"status": "ok"}