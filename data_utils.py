import json


encode_format = "UTF-8"

class DataUtils:

    def serialize_to_json(self, data):
        return json.dumps(data).encode(encode_format)

    def deserialize_json(self, data):
        return json.loads(data)
