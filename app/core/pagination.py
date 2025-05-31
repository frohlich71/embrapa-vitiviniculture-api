from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response model.
    """

    data: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls, data: list[T], total: int, page: int, per_page: int
    ) -> "PaginatedResponse[T]":
        """
        Create a paginated response.
        """
        total_pages = (total + per_page - 1) // per_page  # Ceiling division

        return cls(
            data=data,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )
