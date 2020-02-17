#!/usr/bin/python3

import http.server
import socketserver
import threading
import json
import requests
import sqlite3
import netaddr
from scapy.all import *
import maxminddb

from urllib.parse import urlparse, parse_qs
from datetime import datetime,timedelta
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)
from _sqlite3 import Error

reader = maxminddb.open_database('GeoLite2-City.mmdb')

FILE = 'proxy_test.html'
PORT = 8080
ATLAS_API_KEY = "ba0ea367-df59-4cfb-8e50-3fc8a2fd9243"

API='/api/v1'
MY_RESULTS_REQ=API+'/mine'
PING_START_REQ=API+'/ping'
TRACEROUTE_START_REQ=API+'/traceroute'
PING_RESULT_REQ=API+'/pingresult'
TRACEROUTE_RESULT_REQ=API+'/tracerouteresult'

conn=None
db_file = '0x0B1.db'
db_lock = threading.Lock ()

# /api/v2/measurements/my/?key=ba0ea367-df59-4cfb-8e50-3fc8a2fd9243

def connect_db():
    """ create a database connection to a SQLite database """
    global conn
    

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        conn.execute('''CREATE TABLE IF NOT EXISTS measurements 
             (id int, json text) ''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_json(dbid):
    conn = None
    try:
        db_lock.acquire()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT json FROM measurements WHERE id=%d"%int(dbid))

        rows = cur.fetchall()
        if len(rows) < 1:
            return None
        else:
            return rows[0][0]

    finally:
        if conn is not None:
            conn.close()
        db_lock.release()    

def set_json(dbid, json):
    conn = None
    try:
        db_lock.acquire()
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        sql = ''' INSERT INTO measurements (id,json)
              VALUES(?,?) '''
    
        cur.execute(sql, dbid, json)
    
    finally:
        if conn is not None:
            conn.close()
        db_lock.release()            


class RunReverseTraceroute(threading.Thread):
    def __init__(self,atlas_id):
        super().__init__()
        self.atlas_id = atlas_id

    def run(self):
        print(self.atlas_id)

        json = get_json(self.atlas_id)
        if json is None:
            print("No existing data for %d"%self.atlas_id)
            source = "https://atlas.ripe.net/api/v2/measurements/%d/results/"%self.atlas_id
            responses = requests.get(source).json()
            for response in responses:
                src = netaddr.IPAddress(response['src_addr'])
                if src.is_private():
                    print('private')
                print(src)                
                print(response['dst_addr'])
                valid_dst = None
                for ttl_result in response['result']:
                    print(ttl_result['hop'])
                    if valid_dst is not None:
                        break
                    for result in ttl_result['result']:
                        this_hop = result.get('from')
                        print(this_hop)
                        if this_hop is not None:
                            this_hop_ip = netaddr.IPAddress(this_hop)
                            if this_hop_ip.is_unicast() and not this_hop_ip.is_private():
                                valid_dst = this_hop_ip

                        if valid_dst is not None:
                            break

                if valid_dst is not None:
                    
                    print ("Valid DST: %s" % valid_dst)
                    ans, unans = sr(IP(dst=valid_dst, ttl=(1,25),id=RandShort())/TCP(flags=0x2))
                    for snd,rcv in ans:
                        print (snd.ttl, rcv.src, isinstance(rcv.payload, TCP))








class TestHandler(http.server.SimpleHTTPRequestHandler):
    """The test example handler."""

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
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
        elif TRACEROUTE_START_REQ:
            self.startTraceroute(query_params)
        else:
            print("Invalid Query:")
            print(path)
            self.wfile.write(json.dumps({'type':result_str, 'params': query_params, 'received': 'ok'}).encode())


    def getCity(self, addr):
        response = reader.get(addr)
        if response is not None:
            city = response.get('city')
            country = response.get('country')
            if city :
                city = city.get('names').get('en')
            else:
                city = 'N/A'
            if country :
                country = country.get('names').get('en')
            else:
                country = 'N/A'
            return {"city": city, "country": country, "address": addr}
        else:
            return {"address": addr,"city":"N/A", "country":"N/A"}

    def getPingResults(self, query_params):
        source = "https://atlas.ripe.net/api/v2/measurements/23976423/results/"
        responses = requests.get(source).json()
        for i in responses:
            i['dst_addr'] = self.getCity(i['dst_addr'])
            i['from'] = self.getCity(i['from'])
        self.wfile.write(json.dumps(responses, ensure_ascii=False).encode())

    def getTracerouteResults(self, query_params):
        source = "https://atlas.ripe.net/api/v2/measurements/23976424/results/"
        responses = requests.get(source).json()
        for i in responses:
            dst_addr = i['dst_addr']
            i['dst_addr'] = self.getCity(dst_addr)
            i['from'] = self.getCity(i['from'])
            results = i['result']
            for j in results:
                for k in j['result']:
                    if k.get('from'):
                        k['from'] = self.getCity(k['from'])
        self.wfile.write(json.dumps(responses, ensure_ascii=False).encode())  

    def startTraceroute(self, query_params):
        # localhost:8080/api/v1/traceroute?dest=X.X.X.X&desc=description&proto=TCP
        dest = query_params["dest"][0]
        desc = query_params["desc"][0]
        proto = query_params["proto"][0]

        traceroute = Traceroute(
            af=4,
            target=dest,
            description=desc,
            protocol=proto,
        )

        source = AtlasSource(
            type="area",
            value="WW",
            requested=5,
            tags={"include":["system-ipv4-works"]}
        )

        start_time = datetime.utcnow()+timedelta(0,3)
        atlas_request = AtlasCreateRequest(
            start_time=start_time,
            key=ATLAS_API_KEY,
            measurements=[traceroute],
            sources=[source],
            is_oneoff=True
        )

        (is_success, response) = atlas_request.create()

        print (response)        
        print ("Success ", is_success)
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())         

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
    connect_db()
    start_server()

    # rt = RunReverseTraceroute(23977152)
    # rt.start()
    # rt.join()


