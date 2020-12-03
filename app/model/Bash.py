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
                "key",
                "hash",
                "content"
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
                "depends_on": {
                    "type": ["array"],
                    "items": {
                        "type": ["object", "null"],
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

    def depends_on_check(self, data):
        """
        A security check to remove a depends_on bash that doesn't exist
        :param data:
        :return:
        """
        if "depends_on" in data:
            for elt in data["depends_on"]:
                find = self.find_by({
                    "key": elt
                })
                if find.count() == 0:
                    data["depends_on"].remove(elt)
        return data

    def is_valid(self, data):
        """

        :param data:
        :return:
        """
        # We do a simple pre-check on json schema
        chk = self.validate_input(data)
        if chk[0]:
            # We check the depends-on
            data = self.depends_on_check(data)

        return chk[0], chk[1], data
