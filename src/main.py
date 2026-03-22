from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from src.books import routes


app = FastAPI(
    title="Bookly API",
)

app.include_router(routes.router, prefix="/book")


@app.get("/scalar", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
