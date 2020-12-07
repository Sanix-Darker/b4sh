from b4sh.settings import B4SH_DIR, HOST
from b4sh import *



def save_b4sh(key: str, content: dict):
    """
    To save a b4sh in the b4sh directory
    """
    if len(content) > 1:
        with open("{}/{}.json".format(B4SH_DIR, key), "w") as fii:
            print("content: ", content)
            json.dump(content["result"], fii, indent=4)
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

    r = requests.get("{}/b/r/{}".format(HOST, key))

    status = True if r.status_code == 200 else False
    content = json.loads(r.content.decode().replace('\n', ''))

    if status:
        print("[+] Saving it locally...")
        save_b4sh(key, content)
    else:
        print("[x] Error : {}".format(content["reason"]))
    return status, content


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
        print(payload["content"])


def see_stats(payload):
    """

    """
    choice = input("[?] > See stats (used, updates, up_votes...) ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        get_stats(payload)

def run_content(payload):
    """

    """
    choice = input("[?] > Execute it ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        system(payload["content"])
    else:
        print("[x] Exited !")

def payload_info(key, payload):
    """

    """
    print("[-] Getting : {}...".format(key))
    print("[-] - - -")
    if "author" in payload:
        print("[+] > By {}".format(payload["author"]))

    print("[-] > {}".format(payload["key"]))
    print("[-] > sha256: {}".format(payload["hash"]))

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


def cmd_parser(args: object):
    """

    """

    if args.get != None:
        get(args.get)

    if args.create != None:
        return {
            "key": args.create,
            "method": "create"
        }

    if args.find != None:
        return {
            "key": args.find,
            "method": "find"
        }
