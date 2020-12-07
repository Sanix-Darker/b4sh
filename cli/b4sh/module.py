from b4sh.settings import B4SH_DIR, HOST, VERSION
from b4sh import *


def req_get(url):
    """

    """
    try:
        return requests.get(url, timeout=7)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("[x] No internet connection.")
        return None


def save_b4sh(key: str, content: dict):
    """
    To save a b4sh in the b4sh directory
    """
    if len(content) > 1:
        with open("{}/{}.json".format(B4SH_DIR, key), "w") as fii:
            json.dump(content, fii, indent=4)
            print("[+] Saved content.")
    else:
        print("[x] Not saved, content empty")


def get_saved_b4sh(key: str):
    """

    """
    with open("{}/{}.json".format(B4SH_DIR, key), "r") as fii:
        return fii.read()


def check_b4sh_online(key: str):
    """
    This method will check the b4sh online

    params:
    """
    print("[-] Checking online : {}...".format(key))

    r = req_get("{}/b/r/{}".format(HOST, key))

    if r is not None:
        status = True if r.status_code == 200 else False
        content = json.loads(r.content.decode().replace('\n', ''))

        if status:
            print("[+] Saving it locally...")
            save_b4sh(key, content)
        else:
            print("[x] Error : {}".format(content["reason"]))
        return status, content
    else:
        exit()


def check_b4sh_offline(key: str):
    """

    """
    print("[-] Checking offline : {}...".format(key))

    if path.exists("{}/{}.json".format(B4SH_DIR, key)):
        return True, json.loads(get_saved_b4sh(key))
    else:
        return False, {}


def check_b4sh(key):
    """

    """
    offline_check = check_b4sh_offline(key)
    if offline_check[0]:
        return offline_check
    else:
        online_check = check_b4sh_online(key)
        if online_check[0]:
            return online_check


def get_stats(payload: dict):
    """

    """
    print("[=] Stats:")
    print("[=] ____used_count: {}".format(payload["stats"]["used_count"]))
    print("[=] ____updated_count: {}".format(payload["stats"]["updated_count"]))
    print("[=] ____up_vote: {}".format(payload["stats"]["up_vote"]))
    print("[=] ____down_vote: {}".format(payload["stats"]["down_vote"]))


def see_content(payload):
    """

    """
    choice = input("[?] > See the content ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        print(payload["result"]["content"])


def see_stats(payload):
    """

    """
    choice = input("\n[?] > See stats (used, votes...) ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        get_stats(payload["result"])


def run_content(payload):
    """

    """
    choice = input("[?] > Execute it ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        system(payload["result"]["content"])
    else:
        print("[x] Exited !")


def payload_info(key, payload):
    """

    """

    print("[-] Getting : {}...".format(key))
    print("[-] - - -")
    if "author" in payload:
        print("[+] > By {}".format(payload["result"]["author"]))

    print("[-] > {}".format(payload["result"]["key"]))
    print("[-] > sha256: {}".format(payload["result"]["hash"]))


def get(key: str):
    """
    This method will :
    - check if the b4sh exist locally
    - get the content of a b4sh
    - print details of it
    - execute it

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

def print_results(content: dict):
    """

    """
    print("[+] Listing results ({}) :".format(len(content["result"])))
    for index, elt in enumerate(content["result"]):
        print("[-] {}-) {}".format(index+1, elt["key"]))

    return int(input("\n[?] Your choice (0 to quit):"))


def choose_install(content: dict):
    """

    """
    choice = print_results(content)

    if choice == 0:
        print("[x] Stopping b4sh.")
    else:
        if choice <= len(content["result"]):
            # we try to get that key id bash
            get(content["result"][choice-1]["key"])
        else:
            print("[x] This indice is not correct.")
            exit()

def find(text: str):
    """
    This method will search for available saved commands
    An try to execute them.

    """

    print("[-] Searching for : {}...".format(text))

    r = req_get("{}/b/find?q={}".format(HOST, text))

    status = True if r.status_code == 200 else False
    content = json.loads(r.content.decode().replace('\n', ''))

    if status:
        choose_install(content)
    else:
        print("[x] Error : {}".format(content["reason"]))
        exit()

    return status, content


def list_all():
    """
    List all offline b4sh

    """
    list_offline_b4sh = listdir(B4SH_DIR)

    content = {}
    content["result"] = []
    if len(list_offline_b4sh) > 0:
        for l in list_offline_b4sh:
            with open(B4SH_DIR + "/" + l, "r") as ffk:
                content["result"].append(json.loads(ffk.read())["result"])

        # then we parse results
        choose_install(content)
    else:
        print("[x] 0 offline bash found in {}".format(B4SH_DIR))

def cmd_parser(args: object):
    """

    """
    # we check if the b4sh folder exist
    # if not we install it
    if not path.exists(B4SH_DIR):
        makedirs(B4SH_DIR)

    # the get method
    if args.get is not None:
        get(args.get)

    # the create method
    if args.create is not None:
        return {
            "key": args.create,
            "method": "create"
        }

    # The find method
    if args.find is not None:
        find(args.find)
