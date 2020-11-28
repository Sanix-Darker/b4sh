from app.utils import *
from app.utils.helpers import _del


def upgrade_used(bash_object: dict) -> dict:
    """

    :param bash_object:
    :return: bash_object
    """
    if "stats" in bash_object:
        if "used_count" in bash_object["stats"]:
            bash_object["stats"]["used_count"] += 1

    return bash_object


def get_bash(bash_id: str, password) -> dict:
    """

    :param bash_id:
    :param password:
    :return:
    """
    find = Bash().find_by({
        "bash_id": bash_id
    })

    if find.count() > 0:
        result = check_password(_del("_id", list(find)[0]), password)
    else:
        # the bash doesn't exist at all
        result = {
            "code": "404",
            "reason": "Bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result


def remove_id(elt: dict) -> dict:
    """

    :param elt:
    :return:
    """
    return _del("_id", elt)


def get_all_publics_bash() -> dict:
    """

    :return:
    """
    # we map all over the lit of the cursosr to remove
    # the objecId none serializable object
    result = list(map(remove_id, list(Bash().find_by({
        "password": None
    }))))

    return {
        "code": "200",
        "result": result
    }


def update_and_return_content(key: str, bash: dict):
    """

    :param bash:
    :param key:
    :return:
    """
    # we update the fact that it just have been use
    bash_object = upgrade_used(bash)
    Bash().update({
        "key": key
    }, bash_object)
    Bash().update({
        "history.key": key
    }, bash_object)

    bash_object = _del("bash_id", bash_object)
    bash_object = _del("history", bash_object)

    return {
        "code": "200",
        "result": bash_object
    }


def get_content_by_key(key: str) -> dict:
    """

    :param key:
    :return:
    """
    find = Bash().find_by({
        "key": key
    })

    if find.count() == 0:
        # we need to do a deep search now
        find2 = Bash().find_by({
            "history.key": key
        })
        if find2.count() > 0:
            # we update the fact that it just have been use
            result = update_and_return_content(key, _del("_id", list(find2)[0]))
        else:
            result = {
                "code": "404",
                "reason": "# Sorry but any bash found with that key !"
            }
    else:
        # we update the fact that it just have been use
        result = update_and_return_content(key, _del("_id", list(find)[0]))

    return result
