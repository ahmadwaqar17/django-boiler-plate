import logging
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler that logs all exceptions and ensures
    a consistent JSON format:
    {"success": bool, "error": {"message": str, "code": int}, "data": any}
    """
    
    # Let DRF handle standard API exceptions first to get the default response context
    response = exception_handler(exc, context)

    # Logging
    request = context.get('request')
    view = context.get('view')
    path = request.path if request else 'unknown path'
    logger.error(f"Exception in view {view.__class__.__name__} at {path}: {str(exc)}", exc_info=True)

    # We build the custom payload
    formatted_response = {
        "success": False,
        "error": {
            "message": "A server error occurred.",
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR
        },
        "data": {}
    }

    if response is not None:
        # It's a DRF Exception (ValidationError, NotFound, PermissionDenied, CustomException, etc.)
        formatted_response["error"]["code"] = response.status_code
        
        if isinstance(exc, DRFValidationError):
            formatted_response["error"]["message"] = "Validation Error"
            formatted_response["data"] = response.data # Field specific errors
        else:
            # For general DRF exceptions like NotFound or our UserNotFoundException,
            # the default detail string usually ends up in response.data['detail'].
            if isinstance(response.data, dict) and 'detail' in response.data:
                formatted_response["error"]["message"] = response.data['detail']
            else:
                formatted_response["error"]["message"] = str(exc)
                formatted_response["data"] = response.data
                
        response.data = formatted_response
        return response

    # Handle Django's standard ValidationError (e.g., from model `clean()` or constraints)
    if isinstance(exc, DjangoValidationError):
        formatted_response["error"]["code"] = status.HTTP_400_BAD_REQUEST
        formatted_response["error"]["message"] = "Validation Error"
        
        # Django ValidationError can contain a list of messages or a dict mapping fields to messages
        if hasattr(exc, 'message_dict'):
            formatted_response["data"] = exc.message_dict
        else:
            formatted_response["data"] = {"non_field_errors": exc.messages}
            
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

    # General Python Exceptions (ValueError, TypeError, etc.)
    # We map common ValueError logic used in services.py directly to a 400
    if isinstance(exc, ValueError):
        formatted_response["error"]["code"] = status.HTTP_400_BAD_REQUEST
        formatted_response["error"]["message"] = str(exc)
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

    # Any other unhandled Python exceptions fallback to 500
    formatted_response["error"]["message"] = "An unexpected server error occurred."
    if settings.DEBUG:
        formatted_response["error"]["message"] += f" Detail: {str(exc)}"
        
    return Response(formatted_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.conf import settings
