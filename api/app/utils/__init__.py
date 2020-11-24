# The init module for all CRUD in bash
import uuid
from datetime import datetime
from app.model.Bash import Bash
from random import randint
from app.utils.helpers import *

from app.utils.save_bash import save_bash
from app.utils.get_bash import (
    get_bash,
    get_all_publics_bash,
    get_content_by_key
)
from app.utils.update_bash import update_bash
from app.utils.delete_bash import delete_bash


# Example of a valid bash object
# {
#     "bash_id": "1234",
#     "key": "123:sad",
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
