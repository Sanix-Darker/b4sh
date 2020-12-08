# All helpers in the module
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


def print_results(content: dict):
    """

    :param content:
    :return:
    """
    print("[+] Listing results ({}) :".format(len(content["result"])))
    for index, elt in enumerate(content["result"]):
        print("[-] {}-) {}".format(index + 1, elt["key"]))

    return int(input("\n[?] Your choice (0 to quit):"))


def preset_conf(conf_path: str, conf: dict = {}) -> dict:
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
    payload = {"author": conf["author"], "title": rlinput("[?] Title : ", content_file_path),
               "description": input("[?] Description : ")}
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

    print("[-] Uploading the b4sh ...")

    return payload


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
