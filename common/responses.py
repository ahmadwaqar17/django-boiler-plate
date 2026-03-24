from rest_framework.response import Response

def success_response(data=None, message="Success", status_code=200):
    """
    Returns a consistently formatted success JSON response.
    """
    return Response(
        {
            "success": True,
            "error": None,
            "message": message,
            "data": data if data is not None else {}
        },
        status=status_code
    )

def error_response(message="An error occurred", code=None, status_code=400, data=None):
    """
    Returns a consistently formatted error JSON response.
    """
    return Response(
        {
            "success": False,
            "error": {
                "message": message,
                "code": code or status_code
            },
            "data": data if data is not None else {}
        },
        status=status_code
    )
