from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI(
    title="Bookly API",
    docs_url=None,
    redoc_url=None,
)


@app.get("/")
def hello():
    return {"message": "Hello World."}


@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
