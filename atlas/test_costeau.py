#!/usr/bin/python3
from datetime import datetime,timedelta
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

ATLAS_API_KEY = "ba0ea367-df59-4cfb-8e50-3fc8a2fd9243"

ping = Ping(af=4, target="220.247.159.10", description="Test ping to APRICOT 2020")

traceroute = Traceroute(
    af=4,
    target="220.247.159.10",
    description="Test traceroute to APRICOT 2020",
    protocol="TCP",
)

source = AtlasSource(
    type="area",
    value="WW",
    requested=5,
    tags={"include":["system-ipv4-works"]}
)
source1 = AtlasSource(
    type="country",
    value="NL",
    requested=50,
    tags={"exclude": ["system-anchor"]}
)

start_time = datetime.utcnow()+timedelta(0,3)
atlas_request = AtlasCreateRequest(
    start_time=start_time,
    key=ATLAS_API_KEY,
    measurements=[ping, traceroute],
    sources=[source, source1],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()

print (response)