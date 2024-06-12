from http.server import BaseHTTPRequestHandler, HTTPServer
import json

_url: str = ""


def extract_url(handler):
    global _url
    content_length = int(handler.headers["Content-Length"])
    post_data = handler.rfile.read(content_length)
    json_data = json.loads(post_data.decode("utf-8"))

    _url = json_data["url"]


def run_webserver() -> str:
    httpd = HTTPServer(
        ("", 10043),
        type("", (BaseHTTPRequestHandler,), {"do_POST": extract_url}),
    )

    while not _url:
        httpd.handle_request()

    return _url
