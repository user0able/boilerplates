from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Handler de excepciones que garantiza respuestas de error consistentes."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "error": {
                "status_code": response.status_code,
                "detail": response.data,
            }
        }

    return response
