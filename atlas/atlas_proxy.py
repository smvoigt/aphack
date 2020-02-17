#!/usr/bin/python3

import http.server
import socketserver
import threading
import webbrowser
import json

from urllib.parse import urlparse, parse_qs

FILE = 'proxy_test.html'
PORT = 8080


class TestHandler(http.server.SimpleHTTPRequestHandler):
    """The test example handler."""

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        bits = urlparse(self.path)
        path = bits.path
        query = bits.query
        query_params = parse_qs(query)
        print(path)
        print(query)
        print(query_params)

        result_str = "Invalid Path"
        if path == '/ping':
            result_str="PING"
        elif path == '/traceroute':
            result_str="TRACEROUTE"
        self._set_headers()
        self.wfile.write(json.dumps({'type':result_str, 'params': query_params, 'received': 'ok'}).encode())



def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = http.server.HTTPServer(server_address, TestHandler)
    print("Server starting on localhost:%d"%PORT)
    server.serve_forever()

if __name__ == "__main__":
     start_server()

