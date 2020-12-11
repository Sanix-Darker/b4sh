# To find a b4sh
import json

from b4sh.settings import HOST

from b4sh.utils import *
from b4sh.utils import req_get
from b4sh.utils.get import choose_install


def find(text: str):
    """
    This method will search for available saved commands
    An try to execute them.

    :param text:
    :return:
    """

    print("[-] Searching for : {}...".format(text))

    r = req_get("{}/b/find?q={}".format(HOST, text))

    status = True if r.status_code == 200 or r.status_code == 201 else False
    content = json.loads(r.content.decode().replace('\n', ''))

    if status:
        choose_install(content)
    else:
        print("[x] Error : {}".format(content["reason"]))
        exit()

    return status, content
