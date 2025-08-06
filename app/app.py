import logging

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from base.loggy.core import Loggy
from base.loggy.formatters import JsonFormatter
from third_party.complex_stuff import complex_add


@asynccontextmanager
async def lifespan(_app: FastAPI):

    # Setup logging during startup
    # Loggy.configure(
    #     context={"app": "LoggyTest", "version": "1.0"},
    #     formatter=logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s - context=%(context)s')
    # )

    # Setup logging during startup
    Loggy.configure(
        context={"app": "LoggyTest", "version": "1.0"},
        formatter=JsonFormatter(),
    )

    # Get the third-party logger
    complex_logger = logging.getLogger("complex_stuff")

    #uvicorn_access_logger = logging.getLogger("uvicorn.access")

    Loggy.hijack(complex_logger)
    #Loggy.hijack(uvicorn_access_logger)

    yield  # Run the application


app = FastAPI(lifespan=lifespan)


@app.get("/")
def welcome():
    Loggy.info("Hello world", "Index page visited", extra={"ip": 123, "user_id": 42})
    return {"message": "Hello, world!"}


@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    """
    Add two numbers and log the operation
    """
    result = complex_add(a, b)
    return {"result": result}


def run():
    """
    Run the FastAPI app
    """
    uvicorn.run(app, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    run()
