# Testing the python APIs to ATLAS

## dependencies

pip3 install ripe.atlas.sagan
pip3 install ripe.atlas.cousteau
pip3 install netaddr
pip3 install scapy

## Atlas Proxy (atlas_proxy.py)
Simple python HTTP server to request measurements and see the results

### Ping

#### Start new ping
localhost:8080/api/v1/ping?dest=X.X.X.X&num_sources=10

#### Get result for ping
localhost:8080/api/v1/pingresult?dest=X.X.X.X

### Traceroute

#### Start new
localhost:8080/api/v1/traceroute?dest=X.X.X.X&desc=description&proto=TCP

returns: {"measurements": [23977152]}

#### Get result for traceroute
localhost:8080/api/v1/tracerouteresult?dest=X.X.X.X


## Costeau

https://ripe-atlas-cousteau.readthedocs.io/

First Test: test_costeau.py
 
 ```
 ...

 atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[ping, traceroute],
    sources=[source, source1],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()

{'measurements': [23976423, 23976424]}

 ```


## Sagan

Using sagan we should be able to get the results

