import logging

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from base.loggy.core import Loggy
from third_party.complex_stuff import complex_add


@asynccontextmanager
async def lifespan(_app: FastAPI):

    # Setup logging during startup
    Loggy.configure(
        context={"app": "LoggyTest", "version": "1.0"}
    )

    # Get the third-party logger
    complex_logger = logging.getLogger("complex_stuff")

    # Clear any existing handlers added by the third-party module
    complex_logger.handlers.clear()

    # Set level
    complex_logger.setLevel(logging.DEBUG)

    # Attach your custom handler
    complex_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    complex_handler.setFormatter(formatter)

    # Add new handler
    complex_logger.addHandler(complex_handler)

    # Prevent logs from propagating to the root logger
    complex_logger.propagate = False

    # Attach the complex logger to Loggy
    Loggy.attach(complex_logger)

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
    this is a function so it can be called externally
    by poetry etc
    """
    uvicorn.run(app, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    run()
