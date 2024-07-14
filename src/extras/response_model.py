import json
from pydantic import typing

from fastapi.responses import JSONResponse


class CustomJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any):
        if content is None:
            return bytes()

        if isinstance(content, dict):
            if "status_code" not in content or "result" not in content:
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content,
                }
        elif isinstance(content, str):
            if "status_code" not in content or "result" not in content:
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content,
                }

        elif isinstance(content, list):
            if len(content) != 0 and isinstance(content[0], int):
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content
                }

            elif len(content) != 0 and "count" in content[-1]:
                count = content[-1]['count']
                content.remove(content[-1])
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    "count": count,
                    'result': content
                }
            else:
                content = {
                    'status_code': 200,
                    'message': 'ok',
                    'result': content
                }

        else:
            content = {
                'status_code': 200,
                'message': 'ok',
                'result': content,
            }
        return json.dumps(
            content).encode('utf-8')
