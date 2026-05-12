from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, reports
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pricing Data Analyzer",
    description="API for analyzing pricing data and generating reports",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(reports.router, prefix="/api", tags=["reports"])

@app.get("/")
async def root():
    return {"message": "Pricing Data Analyzer API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
