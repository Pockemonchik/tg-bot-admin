from typing import Annotated, Generic, List, TypeVar

from pydantic import BaseModel, conint
from pydantic.generics import GenericModel


class SuccessAuthUserShema(BaseModel):
    id: int
    username: str
    token: str


class AuthUserShema(BaseModel):
    username: str
    password: str


class PageParams(BaseModel):
    """Request query params for paginated API."""

    page: Annotated[int, conint(ge=1)] = 1
    size: Annotated[int, conint(ge=1, le=100)] = 10


T = TypeVar("T")


class PagedResponseSchema(GenericModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]
