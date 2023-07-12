from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.query_builder import view as query_builder

import uvicorn

allowed_methods = ["GET", "POST", "PUT", "OPTIONS", "DELETE"]
app = FastAPI(
    title="Python API",
    description="This is an API for Python Microservice",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
)


app.include_router(query_builder.router)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=allowed_methods,
                   allow_headers=['*'])


if __name__ == '__main__':
    uvicorn.run(app="main:app", host='0.0.0.0', reload=True)
