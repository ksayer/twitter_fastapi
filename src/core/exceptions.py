from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


class ValidationError(Exception):
    def __init__(
        self,
        model_name: str | None = None,
        message: str | None = None,
        code: int = 422,
        error_type: str = 'Validation Error',
    ):
        self.status_code = code
        self.model_name = model_name
        if model_name:
            self.content = create_exception_message(
                f'{self.model_name} not found', error_type=error_type
            )
        else:
            self.content = create_exception_message(
                message, error_type=error_type  # type: ignore
            )


def register_exception_handlers(app) -> None:
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc) -> JSONResponse:
        """rebuild custom exception to create new message"""
        return JSONResponse(status_code=exc.status_code, content=exc.content)

    @app.exception_handler(RequestValidationError)
    async def pydantic_validation_exception_handler(request, exc) -> JSONResponse:
        """rebuild default pydantic exception to create new message"""
        error = exc.errors()[0]
        message = f"{error['msg']}! location: {error['loc']}"
        return JSONResponse(status_code=422, content=create_exception_message(message))


def create_exception_message(msg: str, error_type: str = 'Validation Error') -> dict:
    return {'result': False, 'error_type': error_type, 'error_message': msg}
