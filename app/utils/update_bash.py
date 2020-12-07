from app.utils import *


def reformat_bash(new_bash_object: dict, bash_object: dict) -> dict:
    """

    :return:
    """
    # we remove the id
    new_bash_object = dell("_id", new_bash_object)

    bash_object["history"] = new_bash_object["history"]
    bash_object["history"].insert(0, {
        "version": len(new_bash_object["history"]) - 1,
        "hash": new_bash_object["hash"],
        "key": new_bash_object["key"],
        "content": new_bash_object["content"],
        "date": new_bash_object["date"],
    })

    bash_object["hash"] = gen_hash(bash_object["content"])
    bash_object["date"] = str(datetime.now())
    if "title" not in bash_object:
        bash_object["title"] = "_" + bash_object["key"]
    else:
        bash_object["key"] = bash_object["title"].strip().replace(" ", "_") + "_" + bash_object["key"]

    bash_object["stats"] = {
        "used_count": new_bash_object["stats"]["used_count"],
        "updated_count": new_bash_object["stats"]["used_count"] + 1,
        "up_vote": new_bash_object["stats"]["up_vote"],
        "down_vote": new_bash_object["stats"]["down_vote"]
    }

    return bash_object


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
        bash = list(find)[0]

        bash_object["bash_id"] = bash_id
        bash_object["key"] = bash["key"]
        bash_object["hash"] = bash["hash"]

        result = check_password(dell("_id", bash), password)
        # if every thing is okay, then we update
        if result["code"] == "200":
            # We do a quick check
            (check_status,
             check_reason,
             bash_object) = Bash().is_valid(bash_object)

            if check_status:
                # we add an element to the history
                # we recompute the hash
                if bash_object["content"] == bash["content"]:
                    result = {
                        "code": "400",
                        "result": "Update can not be done, the content is the same!"
                    }
                else:
                    bash_object = reformat_bash(bash, bash_object)
                    Bash().update({
                        "bash_id": bash_id
                    }, bash_object)
                    result = {
                        "code": "200",
                        "result": "Update on the bash done successfully !"
                    }
            else:
                result = {
                    "code": "400",
                    "reason": "There are some errors with your inputs,"
                              "please check the documentation again ! {}".format(str(check_reason))
                }
    else:
        # the bash doesn't exist at all
        result = {
            "code": "404",
            "reason": "Bash doesn't exist, you can create one using `./b4.sh c`",
        }

    return result


def up_down_vote(bash: dict, up_down: bool) -> dict:
    """

    :param bash:
    :param up_down:
    :return:
    """
    if "stats" in bash:
        if up_down:
            if "up_vote" in bash["stats"]:
                bash["stats"]["up_vote"] += 1
        else:
            if "down_vote" in bash["stats"]:
                bash["stats"]["up_vote"] += 1

    return bash


def vote(key: str, up_down: bool) -> dict:
    """

    :param key:
    :param up_down:
    :return:
    """
    find = Bash().find_by({
        "key": key
    })

    if find.count() > 0:
        Bash().update({
            "key": key
        }, up_down_vote(dell("_id", list(find)[0]), up_down))
        result = {
            "code": "200",
            "result": "Vote done successfully !"
        }
    else:
        find2 = Bash().find_by({
            "history.key": key
        })
        if find2.count() > 0:
            Bash().update({
                "key": key
            }, up_down_vote(dell("_id", list(find2)[0]), up_down))
            result = {
                "code": "200",
                "result": "Vote done successfully !"
            }
        else:
            result = {
                "code": "404",
                "reason": "Any bash with this key found !"
            }
    return result


def down_vote(key: str) -> dict:
    """

    :param key:
    :return:
    """
    return vote(key, False)


def up_vote(key: str) -> dict:
    """

    :param key:
    :return:
    """
    return vote(key, True)
