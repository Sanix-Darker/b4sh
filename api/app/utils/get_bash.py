from app.utils import *

B4 = Bash


def check_password(target: dict, password) -> dict:
    """

    :param target:
    :param password:
    :return:
    """
    if "password" in target:
        if md5(str(password).encode()).hexdigest() == target["password"]:
            del target["password"]
            # the bash have been found with the correct password
            result = {
                "status": "success",
                "code": "200",
                "message": "The bash have been retrieved successfully",
                "result": target
            }
        else:
            # incorrect password
            result = {
                "status": "error",
                "code": "400",
                "message": "The password for this bash is incorrect, please try again !",
            }
    else:
        # successfully retrieve a public bash
        result = {
            "status": "success",
            "code": "200",
            "message": "The bash have been retrieved successfully",
            "result": target
        }

    return result


def get_bash(bash_id: str, password) -> dict:
    """

    :param bash_id:
    :param password:
    :return:
    """
    find = B4().find_by({
        "bash_id": bash_id
    })

    if find.count() > 0:
        target = list(find)[0]
        # we delete some keys
        del target["_id"]
        result = check_password(target, password)
    else:
        # the bash doesn't exist at all
        result = {
            "status": "error",
            "code": "404",
            "message": "Your bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result
