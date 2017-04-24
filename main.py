import requests
import json
import pprint
from secrets.our_secrets import API_KEY, DOMAIN
from schema.schema import SCHEMA
import singer
from jsonschema.exceptions import ValidationError


ENDPOINT = "https://{}.deanslistsoftware.com/api/beta/export/get-behavior-data.php".format(DOMAIN)
params = {
    'apikey': API_KEY
}
dl_request = requests.get(ENDPOINT, params=params)

data = json.loads(dl_request.content.decode('utf-8'))
data = data["data"]

for d in data:
    for k in d:
        if not d[k]:
            d[k] = ""

singer.write_schema('behavior_data', SCHEMA, 'DLSAID')
singer.write_records('behavior_data', data)
# for d in data:
#     try:
#         singer.write_records('behavior_data', d)
#     except ValidationError:
#         print(d)
#         raise