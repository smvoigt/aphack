# Testing the python APIs to ATLAS

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

