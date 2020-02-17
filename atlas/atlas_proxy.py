#!/usr/bin/python3

import http.server
import socketserver
import threading
import json
import requests

from urllib.parse import urlparse, parse_qs

FILE = 'proxy_test.html'
PORT = 8080
ATLAS_API_KEY = "ba0ea367-df59-4cfb-8e50-3fc8a2fd9243"

API='/api/v1'
MY_RESULTS_REQ=API+'/mine'
PING_START_REQ=API+'/ping'
TRACEROUTE_START_REQ=API+'/traceroute'
PING_RESULT_REQ=API+'/pingresult'
TRACEROUTE_RESULT_REQ=API+'/tracerouteresult'

# /api/v2/measurements/my/?key=ba0ea367-df59-4cfb-8e50-3fc8a2fd9243

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

        self._set_headers()
        result_str = "Invalid Path"
        if path == PING_RESULT_REQ:
            self.getPingResults(query_params)
        elif path == TRACEROUTE_RESULT_REQ:
             self.getTracerouteResults(query_params)
        elif path == MY_RESULTS_REQ:
            self.getMyResults(query_params)
        else:
            print("Invalid Query:")
            print(path)
            self.wfile.write(json.dumps({'type':result_str, 'params': query_params, 'received': 'ok'}).encode())

    def getPingResults(self, query_params):
        source = "https://atlas.ripe.net/api/v2/measurements/23976423/results/"
        responses = requests.get(source).json()
        self.wfile.write(json.dumps(responses, ensure_ascii=False).encode())

    def getTracerouteResults(self, query_params):
        source = "https://atlas.ripe.net/api/v2/measurements/23976424/results/"
        responses = requests.get(source).json()
        self.wfile.write(json.dumps(responses, ensure_ascii=False).encode())  

    def getMyResults(self, query_params):
        source = "https://atlas.ripe.net/api/v2/measurements/my/?key=%s"%ATLAS_API_KEY
        responses = requests.get(source).json()
        self.wfile.write(json.dumps(responses, ensure_ascii=False).encode())

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = http.server.HTTPServer(server_address, TestHandler)
    print("Server starting on localhost:%d"%PORT)
    server.serve_forever()

if __name__ == "__main__":
     start_server()

