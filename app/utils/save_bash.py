from app.utils import *


def build_input_bash(input_bash: dict, generated_hash: str) -> dict:
    """

    :param input_bash:
    :param generated_hash:
    :return:
    """
    input_bash["bash_id"] = str(uuid.uuid4())
    input_bash["hash"] = generated_hash

    # we make the key
    input_bash["key"] = generate_key(input_bash["bash_id"], generated_hash)

    input_bash["date"] = str(datetime.now())
    if "title" not in input_bash:
        input_bash["title"] = "_" + input_bash["key"]
    else:
        input_bash["key"] = input_bash["title"].strip().replace(" ", "_") + "_" + input_bash["key"]

    if "password" in input_bash:
        input_bash["password"] = md5(input_bash["password"].encode()).hexdigest()

    input_bash["stats"] = {
        "used_count": 0,
        "updated_count": 0,
        "up_vote": 0,
        "down_vote": 0
    }

    # we append the first version of the history in the bash object
    input_bash["history"] = [{
        "version": 0,
        "hash": generated_hash,
        "key": input_bash["key"],
        "content": input_bash["content"],
        "date": input_bash["date"],
    }]

    return input_bash


def validate_before_save(input_bash: dict) -> dict:
    """

    :param b4:
    :param input_bash:
    :return:
    """
    (check_status,
     check_reason,
     input_bash) = Bash().is_valid(input_bash)

    # Let's validate the input
    if check_status:
        # Then save
        Bash(input_bash).save()
        input_bash = dell("_id", input_bash)
        input_bash = dell("history", input_bash)
        result = {
            "code": "201",
            "result": input_bash
        }
    else:
        result = {
            "code": "400",
            "reason": "There are some errors with your inputs,"
                      "please check the documentation again ! {}".format(str(check_reason))
        }

    return result


def save_bash(input_bash: dict) -> dict:
    """

    :param input_bash:
    :return:
    """
    # We verify if all required are there
    if "content" in input_bash and len(input_bash["content"]) > 2:
        # A security check for too high characters
        if len(input_bash["content"]) > 15000:
            result = {
                "code": "400",
                "reason": "The 'content' exceed the limit of characters it can not be saved !"
            }
        else:
            # we generate the hash of the content
            generated_hash = gen_hash(input_bash["content"])

            # We build our input_bash
            input_bash = build_input_bash(input_bash, generated_hash)

            # We validate before save the bash
            result = validate_before_save(input_bash)
    else:
        result = {
            "code": "400",
            "reason": "At least, please specify the 'content' of your bash!"
        }

    return result
