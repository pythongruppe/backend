import json
from flask import Response


def json_error(message, http_code, error=None):
    response_content = json.dumps({'message': message, 'code': http_code, 'error': str(error) if error else None})
    return Response(response_content, http_code)
