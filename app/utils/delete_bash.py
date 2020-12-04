from app.utils import *


def check_password_and_delete(target: dict, password) -> dict:
    """

    :param target:
    :param password:
    :return:
    """
    if "password" in target:
        if md5(str(password).encode()).hexdigest() == target["password"]:
            target = dell(target["password"])
            Bash().delete({
                "bash_id": target["bash_id"]
            })
            # the bash have been found with the correct password
            result = {
                "code": "200",
                "result": "The bash have been deleted successfully",
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
            "code": "403",
            "reason": "This is a public bash, you can't delete it, even if you're the author",
        }

    return result


def delete_bash(bash_id, password):
    find = Bash().find_by({
        "bash_id": bash_id
    })

    if find.count() > 0:
        target = list(find)[0]
        # we delete some keys
        del target["_id"]
        result = check_password_and_delete(target, password)
    else:
        # the bash doesn't exist at all
        result = {
            "code": "404",
            "reason": "Your bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result
