import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from base.loggy import Loggy


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Setup logging during startup
    Loggy.configure(
        context={"app": "LoggyTest", "version": "1.0"}
    )

    yield  # Run the application


app = FastAPI(lifespan=lifespan)


@app.get("/")
def welcome():
    Loggy.info("Hello world", "Index page visited", extra={"ip": 123, "user_id": 42})
    return {"message": "Hello, world!"}


def run():
    """
    Run the FastAPI app
    this is a function so it can be called externally
    by poetry etc
    """
    uvicorn.run(app, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    run()
