from app.utils import *
from app.utils.helpers import _del


def update_bash(bash_id: str, bash_object: dict, password) -> dict:
    """

    :param bash_object:
    :param bash_id:
    :param password:
    :return:
    """
    find = Bash().find_by({
        "bash_id": bash_id
    })

    if find.count() > 0:
        result = check_password(_del("_id", list(find)[0]), password)
        # if every thing is okay, then we update
        if result["code"] == "200":
            Bash().update({
                "bash_id": bash_id
            }, bash_object)
            result = {
                "code": "200",
                "result": bash_object
            }
    else:
        # the bash doesn't exist at all
        result = {
            "code": "404",
            "reason": "Bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result
