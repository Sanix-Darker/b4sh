from app.model import Model


class Bash(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        
        # We set the collection name
        self.set_collection("bashs")

        # We set our custom schema
        # the stats contain here used_count, updated_count, up_vote, down_vote
        # history is an array of all precedent instance of the same bash object
        self.schema = {
            "type": "object",
            "required": [
                "bash_id",
                "hash",
                "content",
                "stats",
                "history",
                "date"
            ],
            "properties": {
                "bash_id": {"type": "string"},
                "key": {"type": "string"},
                "password": {"type": "string"},
                "hash": {"type": "string"},
                "title": {"type": "string"},
                "author": {"type": "string"},
                "description": {"type": "string"},
                "content": {"type": "string"},
                "stats": {
                    "type": ["object"],
                    "items": {
                        "used_count": ["number", "null"],
                        "updated_count": ["number", "null"],
                        "up_vote": ["number", "null"],
                        "down_vote": ["number", "null"],
                    }
                },
                "history": {
                    "type": ["array"],
                    "items": {
                        "type": ["object", "null"],
                    }
                },
                "date": {"type": "string"}
            }
        }
