# To list all available bash commands
import json

from b4sh.settings import *
from b4sh.utils import *
from b4sh.utils.get import choose_install


def list_all():
    """
    List all offline b4sh

    :return:
    """
    list_offline_b4sh = listdir(B4SH_DIR)

    content = {"result": []}
    if len(list_offline_b4sh) > 0:
        for l in list_offline_b4sh:
            # we escape the configuration file
            if "conf.json" not in l:
                with open(B4SH_DIR + "/" + l, "r") as ffk:
                    cnt = json.loads(ffk.read())
                    content["result"].append(cnt["result"])

        # then we parse results
        choose_install(content)
    else:
        print("[x] 0 offline bash found in {}".format(B4SH_DIR))
