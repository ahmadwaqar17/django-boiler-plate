from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    """
    Custom renderer to ensure all successful API responses follow a consistent format:
    {
        "success": True,
        "error": None,
        "message": "Success",
        "data": { ... } or [ ... ]
    }
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')
        
        # If the response is already in the custom format (e.g. from common.responses or exception handler), 
        # don't wrap it again.
        if isinstance(data, dict) and all(k in data for k in ["success", "error", "data"]):
            return super().render(data, accepted_media_type, renderer_context)

        # Only wrap successful responses (2xx status codes)
        # Error responses (4xx, 5xx) are handled by common.exception_handlers.custom_exception_handler
        if response and 200 <= response.status_code < 300:
            formatted_data = {
                "success": True,
                "error": None,
                "message": "Success",
                "data": data if data is not None else {}
            }
            return super().render(formatted_data, accepted_media_type, renderer_context)

        # Fallback to default rendering for other statuses (though they should be handled by exception handler)
        return super().render(data, accepted_media_type, renderer_context)
