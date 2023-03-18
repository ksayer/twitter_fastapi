from typing import Any, Mapping

response_422: Mapping[int | str, dict[str, Any]] = {
    422: {
        'description': 'Validation Error',
        'content': {
            'application/json': {
                'schema': {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "boolean",
                            "enum": False,
                        },
                        "error_type": {
                            "type": "string",
                        },
                        "error_message": {
                            "type": "string",
                        },
                    },
                    "example": {
                        "result": False,
                        "error_type": "ValidationError",
                        "error_message": "user not found",
                    },
                },
            },
        },
    },
}

simple_response_200: Mapping[int | str, dict[str, Any]] = {
    200: {
        'description': 'Success response',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'result': {
                            'type': 'boolean',
                            'enum': False,
                        },
                    },
                    'example': {
                        'result': True,
                    },
                },
            },
        },
    },
}


response_403: Mapping[int | str, dict[str, Any]] = {
    403: {
        'description': 'Forbidden',
        'content': {
            'application/json': {
                'schema': {
                    "type": "object",
                    "properties": {
                        "result": {
                            "type": "boolean",
                            "enum": False,
                        },
                        "error_type": {
                            "type": "string",
                        },
                        "error_message": {
                            "type": "string",
                        },
                    },
                    "example": {
                        "result": False,
                        "error_type": "Forbidden",
                        "error_message": "Authorization required",
                    },
                },
            },
        },
    },
}
