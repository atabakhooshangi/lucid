import json
from pydantic import typing
from fastapi.responses import JSONResponse

class CustomJSONResponse(JSONResponse):
    """
    Custom JSON response class that standardizes the response format.

    Inherits from FastAPI's JSONResponse and modifies the render method to ensure
    the response content follows a consistent structure.
    """
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        """
        Render the content into a JSON-formatted byte string.

        Args:
            content (typing.Any): The content to be rendered into the response.

        Returns:
            bytes: The JSON-encoded response content.
        """
        if content is None:
            return bytes()

        if isinstance(content, dict):
            # Ensure the dictionary includes 'status_code' and 'result' keys
            if "status_code" not in content or "result" not in content:
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content,
                }
        elif isinstance(content, str):
            # Ensure the string content is wrapped in a dictionary with 'status_code' and 'result' keys
            content = {
                'status_code': 200,
                'message': 'ok',
                'result': content,
            }
        elif isinstance(content, list):
            if len(content) != 0 and isinstance(content[0], int):
                # List of integers, wrap in dictionary with 'status_code' and 'result' keys
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content
                }
            elif len(content) != 0 and "count" in content[-1]:
                # List of items with a 'count' key in the last item, extract count and wrap in dictionary
                count = content[-1]['count']
                content.remove(content[-1])
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    "count": count,
                    'result': content
                }
            else:
                # General list, wrap in dictionary with 'status_code' and 'result' keys
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content
                }
        else:
            # General case for other types, wrap in dictionary with 'status_code' and 'result' keys
            content = {
                'status_code': 200,
                'message': 'ok',
                'result': content,
            }
        return json.dumps(content).encode('utf-8')
