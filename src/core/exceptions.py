from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


class ValidationError(Exception):
    def __init__(self, model_name, code: int = 400):
        self.status_code = code
        self.model_name = model_name
        self.content = create_exception_message(f'{self.model_name} not found')


def register_exception_handlers(app) -> None:
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=exc.content)

    @app.exception_handler(RequestValidationError)
    async def pydantic_validation_exception_handler(request, exc) -> JSONResponse:
        error = exc.errors()[0]
        message = f"{error['msg']}! location: {error['loc']}"
        return JSONResponse(status_code=400, content=create_exception_message(message))


def create_exception_message(msg: str) -> dict:
    return {'result': False, 'error_type': 'ValidationError', 'error_message': msg}
