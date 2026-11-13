from fastapi import FastAPI
from app.api import strategies, trades, analytics

app = FastAPI(
    title="Algorithmic Trading & Performance Analytics Platform",
    version="1.0.0"
)

# Include all API routers
app.include_router(strategies.router)
app.include_router(trades.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Titan Quant Research Lab Backend is live!"}