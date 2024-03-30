from dataclasses import dataclass

from fastapi import HTTPException


class HTTPError(HTTPException):
    def __init__(
        self,
        status_code: int,
        *,
        errors: list[str],
        detail: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        (
            super().__init__(
                status_code=status_code, detail=detail, headers=headers
            ),
        )
        self.errors = errors


@dataclass
class ApplicationException(Exception):
    status_code: int
    message_text: str

    @property
    def message(self):
        return f"An error has been occured: {self.message_text}"


class RepositoryException(ApplicationException):
    pass
