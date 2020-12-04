import sys
import traceback
from hashlib import sha256, md5
from random import randint


def get_trace():
    print("Exception in code:")
    print("-" * 60)
    traceback.print_exc(file=sys.stdout)
    print("-" * 60)


def gen_hash(_str: str) -> str:
    """

    :param _str:
    :return:
    """
    return sha256(_str.encode()).hexdigest()


def generate_key(bash_id: str, generated_hash: str):
    """

    :param bash_id:
    :param generated_hash:
    :return:
    """
    separator = [":", "|", "_", "]", "[", "%", "@", "$", "#", "!", "}", "{"]
    key = bash_id[:2]
    key += separator[randint(0, len(separator) - 1)] + generated_hash[:2]
    key = md5(key.encode()).hexdigest()[:5]

    return key


def dell(key: str, _object: object):
    try:
        if key in _object:
            del _object[key]
        else:
            print("[x] {} not in object.".format(key))
    except Exception as es:
        print(es)
        get_trace()

    return _object


def check_password(target: dict, password) -> dict:
    """

    :param target:
    :param password:
    :return:
    """
    if "password" in target:
        if md5(str(password).encode()).hexdigest() == target["password"]:
            # the bash have been found with the correct password
            result = {
                "code": "200",
                "result": dell("password", target)
            }
        else:
            # incorrect password
            result = {
                "code": "400",
                "reason": "The password for this bash is incorrect, please try again !",
            }
    else:
        # successfully retrieve a public bash
        result = {
            "code": "200",
            "result": target
        }

    return result

