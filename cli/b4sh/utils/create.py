from b4sh.utils import *


def save_b4sh_offline(key: str, content: dict):
    """
    To save a b4sh in the b4sh directory

    :param key:
    :param content:
    :return:
    """
    if len(content) > 1:
        with open("{}/{}.json".format(B4SH_DIR, key), "w") as fii:
            json.dump(content, fii, indent=4)
            print("[+] Saved content.")
    else:
        print("[x] Not saved, content empty")


def get_saved_b4sh(key: str):
    """

    :param key:
    :return:
    """
    with open("{}/{}.json".format(B4SH_DIR, key), "r") as fii:
        return fii.read()


def check_b4sh_online(key: str):
    """
    This method will check the b4sh online

    :param key:
    :return:
    """
    print("[-] Checking online : {}...".format(key))

    r = req_get("{}/b/r/{}".format(HOST, key))

    if r is not None:
        status = True if r.status_code == 200 or r.status_code == 201 else False
        content = json.loads(r.content.decode().replace('\n', ''))

        if status:
            print("[+] Saving it locally...")
            save_b4sh_offline(key, content)
        else:
            print("[x] Error : {}".format(content["reason"]))
        return status, content
    else:
        exit()


def check_b4sh_offline(key: str):
    """

    :param key:
    :return:
    """
    print("[-] Checking offline : {}...".format(key))

    if path.exists("{}/{}.json".format(B4SH_DIR, key)):
        return True, json.loads(get_saved_b4sh(key))
    else:
        return False, {}


def check_b4sh(key):
    """

    :param key:
    :return:
    """
    offline_check = check_b4sh_offline(key)
    if offline_check[0]:
        return offline_check
    else:
        online_check = check_b4sh_online(key)
        if online_check[0]:
            return online_check


def create_b4sh(content_file_path: str = ""):
    """

    :param content_file_path:
    :return:
    """
    # The configuration set
    conf = ask_set_conf()
    # if it doesn't exist we create it
    print("[-] " + "-" * 20)
    print("[-] author : {}".format(conf["author"]))
    print("[-] os-pid : {}".format(conf["pid"]))
    print("[-] " + "-" * 20)

    print("\n[+] Creating a new b4sh...")
    print("")
    # We format and get the payload

    r = req_post("{}/b".format(HOST), get_format_payload(conf, content_file_path))

    status = True if r.status_code == 200 or r.status_code == 201 else False
    content = json.loads(r.content.decode().replace('\n', ''))

    if status:
        print("[+] b4sh {} created/saved successfully !".format(content["result"]["key"]))
        with open(B4SH_DIR + "/" + content["result"]["key"] + ".json", "w") as fik:
            json.dump(content, fik, indent=4)
    else:
        print("[x] Error : {}".format(content["reason"]))
        exit()
