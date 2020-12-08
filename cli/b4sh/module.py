from b4sh.settings import B4SH_DIR, HOST, VERSION
from b4sh import *
import readline


def req_get(url):
    """

    :param url:
    :return:
    """
    try:
        return requests.get(url, timeout=7)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("[x] No internet connection.")
        return None


def paste_help():
    """

    :return:
    """
    print("""
usage: b4sh [-h] [-g GET] [-f FIND] [-c CREATE] [-ls LIST] [-v]

optional arguments:
  -h,  --help    Show this help message and exit.

  -g,  --get     To get a b4sh by key/id, Ex: b4sh -g apache2_eerft.

  -f,  --find    To find a b4sh by name online, Ex: b4sh -f nginx.

  -c,  --create  To create a new B4sh, Ex: b4sh -c / Or with a file_path, Ex: b4sh -c script.sh

  -ls, --list    To list all available offline/local b4sh shells.

  -v,  --version To get the actual version of b4sh.
    """)


def req_post(url, dat):
    """

    :param url:
    :param dat:
    :return:
    """
    try:
        return requests.post(url, json=dat, timeout=10)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("[x] No internet connection.")
        return None


def save_b4sh(key: str, content: dict):
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
            save_b4sh(key, content)
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


def get_stats(payload: dict):
    """

    :param payload:
    :return:
    """
    print("[=] Stats:")
    print("[=] ____used_count: {}".format(payload["stats"]["used_count"]))
    print("[=] ____updated_count: {}".format(payload["stats"]["updated_count"]))
    print("[=] ____up_vote: {}".format(payload["stats"]["up_vote"]))
    print("[=] ____down_vote: {}".format(payload["stats"]["down_vote"]))


def see_content(payload):
    """

    :param payload:
    :return:
    """
    choice = input("[?] > See the content ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        print(payload["result"]["content"])


def see_stats(payload):
    """

    :param payload:
    :return:
    """
    choice = input("\n[?] > See stats (used, votes...) ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        get_stats(payload["result"])


def run_content(payload):
    """

    :param payload:
    :return:
    """
    choice = input("[?] > Execute it ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        system(payload["result"]["content"])
    else:
        print("[x] Exited !")


def payload_info(key, payload):
    """

    :param key:
    :param payload:
    :return:
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


def print_results(content: dict):
    """

    :param content:
    :return:
    """
    print("[+] Listing results ({}) :".format(len(content["result"])))
    for index, elt in enumerate(content["result"]):
        print("[-] {}-) {}".format(index + 1, elt["key"]))

    return int(input("\n[?] Your choice (0 to quit):"))


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


def list_all():
    """
    List all offline b4sh

    :return:
    """
    list_offline_b4sh = listdir(B4SH_DIR)

    content = {}
    content["result"] = []
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


def preset_conf(conf_path: str, conf: dict={}) -> dict:
    """

    :param conf_path:
    :param conf:
    :return:
    """
    if "author" not in conf:
        print("[+] Please give me a username that will be save next time as author of your scripts.")
        conf["author"] = str(input("[?] author : "))

    if "pid" not in conf:
        conf["pid"] = str(getpid())

    with open(conf_path, "w") as fil:
        json.dump(conf, fil, indent=4)

    return conf


def ask_set_conf():
    """

    :return:
    """
    # We try to open the config file
    conf_path = B4SH_DIR + "/" + "conf.json"
    if path.exists(conf_path):
        with open(conf_path, "r") as fil:
            return preset_conf(conf_path, json.loads(fil.read()))
    else:
        return preset_conf(conf_path)


def rlinput(prompt, prefill=''):
    """

    :param prompt:
    :param prefill:
    :return:
    """
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
        readline.set_startup_hook()


def get_content():
    """

    :return:
    """
    print("[?] Content** ( In a new line, Ctrl-D to save the content ): ")

    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    return '\n'.join(contents)


def get_format_payload(conf: dict, content_file_path: str = "") -> dict:
    """

    :param conf:
    :param content_file_path:
    :return:
    """
    payload = {}
    payload["author"] = conf["author"]
    payload["title"] = rlinput("[?] Title : ", content_file_path)
    payload["description"] = input("[?] Description : ")
    if len(content_file_path) > 2:
        # we check if the path of the shell file exist
        if not path.exists(content_file_path):
            print("[x] The file-path you provided is not correct !")
            print("[-] Try to write your commands mannualy !")
            payload["content"] = get_content()
        else:
            print("[+] Getting the content...")
            with open(content_file_path, "r") as fr:
                payload["content"] = fr.read()
    else:
        payload["content"] = get_content()

    return payload


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
        with open(B4SH_DIR + "/" + content["result"]["key"] + "json", "w") as fik:
            json.dump(content, fik, indent=4)
    else:
        print("[x] Error : {}".format(content["reason"]))
        exit()


def cmd_parser(args: object):
    """

    :param args:
    :return:
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
