from fastapi import HTTPException


def validate_body_not_empty(body: str) -> None:
    if body is None or body.strip() == "":
        raise HTTPException(
            status_code=422,
            detail="body cannot be empty"
        )
