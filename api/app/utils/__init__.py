# The init module for all CRUD in bash
from app.utils.save_bash import save_bash
from app.utils.get_bash import get_bash
from app.utils.update_bash import update_bash
from app.utils.delete_bash import delete_bash

# Example of a valid bash object
# {
#     "bash_id": "1234",
#     "bash_short_id": "123:sad",
#     "hash": "sadoisankjcn2798382hnkjsacndskjcndsccdsc",
#     "title": "A simple echo",
#     "author": "d4rk3r",
#     "description": "This is a test of the echo command",
#     "content": "echo 'test'",
#     "stats": {
#         "used_count": 3,
#         "updated_count": 1,
#         "up_vote": 17,
#         "down_vote": 3,
#     },
#     "history": [],
#     "date": "2020-04-11 04:47:09"
# }
