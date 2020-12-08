# To get a b4sh command list
from b4sh.utils import *
from b4sh.utils.create import check_b4sh


def get(key: str):
    """
    This method will :
        - check if the b4sh exist locally
        - get the content of a b4sh
        - print details of it
        - execute it

    :param key:
    :return:
    """
    # We check if the b4sh exist locally
    chk = check_b4sh(key)

    if chk is not None:
        if chk[0]:
            payload = chk[1]
            # print little infos for the payload
            payload_info(key, payload)

            # A method to see the content
            see_content(payload)

            # A method to see stats
            see_stats(payload)

            # To run content
            run_content(payload)
        else:
            print("[x] This b4sh seems to not exist !")
    else:
        print("[x] This b4sh seems to not exist !")


def choose_install(content: dict):
    """

    :param content:
    :return:
    """
    choice = print_results(content)

    if choice == 0:
        print("[x] Stopping b4sh.")
    else:
        if choice <= len(content["result"]):
            # we try to get that key id bash
            get(content["result"][choice - 1]["key"])
        else:
            print("[x] This indice is not correct.")
            exit()
