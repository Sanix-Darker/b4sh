from app.utils import *


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
        result = check_password(dell("_id", list(find)[0]), password)
    else:
        # the bash doesn't exist at all
        result = {
            "code": "404",
            "reason": "Bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result


def find_b4sh(string: str, password) -> dict:
    """
    This method will fetch on title field for b4sh

    :param string:
    :return:
    """
    result = {}
    if password is not None:
        result = list(map(remove_id, list(Bash().find_by({
            "title": {'$regex': string},
            "password": password
        }))))
    else:
        result = list(map(remove_id, list(Bash().find_by({
            "title": {'$regex': string}
        }))))

    return {
        "code": "200",
        "result": result
    }


def remove_id(elt: dict) -> dict:
    """

    :param elt:
    :return:
    """
    return dell("_id", elt)


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


def get_all_private_bash(password: str) -> dict:
    """

    :return:
    """
    # we map all over the lit of the cursosr to remove
    # the objecId none serializable object
    result = list(map(remove_id, list(Bash().find_by({
        "password": password
    }))))

    return {
        "code": "200",
        "result": result
    }


def append_content_depending_on(bash_object: dict) -> str:
    """

    :param bash_object:
    :return:
    """
    content = ""
    if "depends_on" in bash_object:
        # we check if the bash is a list or something else
        if type(bash_object["depends_on"]) == list:
            for elt in bash_object["depends_on"]:
                find = Bash().collection.find({
                    "key": {'$regex': elt}
                })

                if find.count() == 0:
                    try:
                        bash_object["depends_on"].remove(elt)
                    except Exception as es:
                        get_trace()

                    content += " \n# Bash - {} doesn't exist".format(elt)
                else:
                    content += " \n# Depends on {} \n{}".format(elt, list(find)[0]["content"])
        else:
            content += " \n# Bash - {} doesn't exist".format(bash_object["depends_on"])

    return content


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

    bash_object = dell("bash_id", bash_object)
    bash_object = dell("history", bash_object)

    # We append contents if there is some dependencies
    bash_object["content"] = append_content_depending_on(bash_object) + " \n" + bash_object["content"]

    return {
        "code": "200",
        "result": bash_object
    }


def get_content_by_key(key: str) -> dict:
    """

    :param key:
    :return:
    """
    find = Bash().collection.find({
        "key": {'$regex': key}
    })

    if find.count() == 0:
        # we need to do a deep search now
        find2 = Bash().collection.find({
            "history.key": {'$regex': key}
        })

        if find2.count() > 0:
            # we update the fact that it just have been use
            result = update_and_return_content(key, dell("_id", list(find2)[0]))
        else:
            result = {
                "code": "404",
                "reason": "# Sorry but any bash found with that key !"
            }
    else:
        # we update the fact that it just have been use
        result = update_and_return_content(key, dell("_id", list(find)[0]))

    return result
