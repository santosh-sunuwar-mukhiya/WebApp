from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from book_data import books
from schemas import Book, CreateBook, UpdateBook

app = FastAPI(
    title="Bookly API",
)


@app.get("/books", response_model=list[Book])
def get_all_books():
    return books


@app.post("/book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(create: CreateBook):
    max_id = 0
    for book in books:
        if book["id"] > max_id:
            max_id = book["id"]

    new_id = max_id + 1

    new_book = {"id": new_id, **create.model_dump()}

    books.append(new_book)

    return new_book


@app.get("/scalar", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
