import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from services.xaqlTabobat.XalqTabobat import modelTib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(modelTib)

