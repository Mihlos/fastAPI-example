from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel


class Book(BaseModel):
    name: str
    price: float = 10.0
    date: datetime


book1 = {
    "name": "book1",
    "price": 11.1,
    "date": datetime.today()
}

book_object = Book(**book1)


def print_book(book: Book):
    print(book)


print_book(book_object)
