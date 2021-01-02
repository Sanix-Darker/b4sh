# All helpers in the module
from b4sh import *
import readline
from math import ceil


def req_get(url):
    """
    A simple method to make a GET request
    With a try-except if the request doesn't succeed

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
    A simple method to make a POST request
    With a try-except if the request doesn't succeed

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
    Same as input  but will add a prefill as a placehoder

    :param prompt:
    :param prefill:
    :return:
    """
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)  # or raw_input in Python 2
    finally:
        readline.set_startup_hook()


def see_content(payload):
    """
    A method to print or not the content

    :param payload:
    :return:
    """
    choice = input("[?] > See the content ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        print(payload["result"]["content"])


def see_stats(payload):
    """
    Just a print for stats on a b4sh

    :param payload:
    :return:
    """
    choice = input("\n[?] > See stats (used, votes...) ? (Y/N): ")
    if choice.lower() == "y" or choice.lower() == "yes":
        print("[=] Stats:")
        print("[=] ____used_count: {}".format(payload["result"]["stats"]["used_count"]))
        print("[=] ____updated_count: {}".format(payload["result"]["stats"]["updated_count"]))
        print("[=] ____up_vote: {}".format(payload["result"]["stats"]["up_vote"]))
        print("[=] ____down_vote: {}".format(payload["result"]["stats"]["down_vote"]))


def run_content(payload):
    """
    To run the content of a b4sh

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
    This method will get infos of a payload

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
    Listing results of a request

    :param content:
    :return:
    """
    print("[+] Listing results ({}) :".format(len(content["result"])))
    # for index, elt in enumerate(content["result"]):
    #     print("[-] {}-) {}".format(index + 1, elt["key"]))
    list_columns(content["result"])

    return int(input("\n[?] Your choice (0 to quit):"))


def preset_conf(conf_path: str, conf: dict = {}) -> dict:
    """
    This method is for setting pre-configuration

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
    Just to ask if yes or no we should set conf for unexistance configurations

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
    To get the input content

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
    payload = {
        "author": conf["author"],
        "title": rlinput("[?] Title : ", content_file_path.replace("./", "")),
        "description": input("[?] Description : ")
    }
    if len(content_file_path) > 2:
        # we check if the path of the shell file exist
        if not path.exists(content_file_path):
            print("[x] The file-path you provided is not correct !")
            print("[-] Try to write your commands manually !")
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
usage: b (or b4sh) [-h] [-g GET] [-f FIND] [-c CREATE] [-ls LIST] [-v]

optional arguments:
  -h,  --help    Show this help message and exit.
  -g,  --get     To get a b4sh by key/id, Ex: b4sh -g apache2_eerft.
  -f,  --find    To find a b4sh by name online, Ex: b4sh -f nginx.
  -r,  --run     To run directly with the good key/id, Ex: b4sh -r nginx_eedrf4.
  -c,  --create  To create a new B4sh, Ex: b4sh -c / Or with a file_path, Ex: b4sh -c script.sh
  -ls, --list    To list all available offline/local b4sh shells.
  -v,  --version To get the actual version of b4sh.
    """)


def list_columns(obj, cols=4, columnwise=True, gap=4):
    """
    Print the given list in evenly-spaced columns.

    Parameters
    ----------
    obj : list
        The list to be printed.
    cols : int
        The number of columns in which the list should be printed.
    columnwise : bool, default=True
        If True, the items in the list will be printed column-wise.
        If False the items in the list will be printed row-wise.
    gap : int
        The number of spaces that should separate the longest column
        item/s from the next column. This is the effective spacing
        between columns based on the maximum len() of the list items.
    """

    sobj = [" " + str(index+1) + "-) " + str(item["key"]) for index, item in enumerate(obj)]
    if cols > len(sobj):
        cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise:
        cols = int(ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n'.join([''.join([c.ljust(max_len + gap) for c in p]) for p in plist])

    print(printer)
