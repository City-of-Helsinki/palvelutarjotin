import json
from urllib.parse import parse_qs, urlsplit


def format_request(request):
    return json.dumps(request)


def get_params_from_url(url: str):
    query = urlsplit(url).query
    params = parse_qs(query)
    return dict(params)
