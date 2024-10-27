import json
from crypt import methods

from bson import json_util


class Serializer:

    def __init__(self, data):
        self.data = data

    def serialize(self) -> dict:
        return dict(self.data)

    def deserialize(self, encoding='utf-8') -> dict:
        return json_util.loads(json.dumps(self.data, default=str, indent=4).encode(encoding))
