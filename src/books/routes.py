from fastapi import APIRouter, status, HTTPException

from src.books.book_data import books
from src.books.schemas import Book, CreateBook, UpdateBook

router = APIRouter()


@router.get("/", response_model=list[Book])
def get_all_books():
    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(create: CreateBook):
    max_id = 0
    for book in books:
        if book["id"] > max_id:
            max_id = book["id"]

    new_id = max_id + 1

    new_book = {"id": new_id, **create.model_dump()}

    books.append(new_book)

    return new_book


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")


@router.patch("/{book_id}", response_model=Book)
def update_book(book_id: int, update: UpdateBook):
    # 1. Find the book
    for index, book in enumerate(books):
        if book["id"] == book_id:
            # 2. Extract ONLY the fields the user actually sent in the request
            # exclude_unset=True ignores any field not explicitly provided by the user
            update_data = update.model_dump(exclude_unset=True)

            # 3. Create a copy of the existing book and update it with the new data
            # This keeps all the old values for fields not present in update_data
            updated_book = {**book, **update_data}

            # 4. Save it back to your storage
            books[index] = updated_book

            return updated_book

    raise HTTPException(status_code=404, detail="Book not found.")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    # 1. Loop through the list using the index (0, 1, 2...)
    for index in range(len(books)):

        # 2. Check if the book at this index has the ID we want
        if books[index]["id"] == book_id:

            # 3. Remove the item at this specific position
            books.pop(index)

            # 4. Return immediately so we don't keep looping
            # (204 No Content doesn't require a return body)
            return

    # 5. If the loop finishes and we haven't returned, the ID doesn't exist
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
