from fastapi import FastAPI
from app.api import router


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
