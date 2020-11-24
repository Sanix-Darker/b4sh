from app.utils import *

B4 = Bash


def check_password_and_delete(target: dict, password) -> dict:
    """

    :param target:
    :param password:
    :return:
    """
    if "password" in target:
        if md5(str(password).encode()).hexdigest() == target["password"]:
            del target["password"]
            B4().delete({
                "bash_id": target["bash_id"]
            })
            # the bash have been found with the correct password
            result = {
                "status": "success",
                "code": "200",
                "message": "The bash have been deleted successfully",
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
            "status": "error",
            "code": "403",
            "message": "This is a public bash, you can't delete it, even if you're the author",
            "result": target
        }

    return result


def delete_bash(bash_id, password):
    find = B4().find_by({
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
            "status": "error",
            "code": "404",
            "message": "Your bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result
