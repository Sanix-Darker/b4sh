from app.utils import *


B4 = Bash


def build_input_bash(input_bash: dict, generated_hash: str) -> dict:
    """

    :param input_bash:
    :param generated_hash:
    :return:
    """
    input_bash["bash_id"] = str(uuid.uuid4())
    input_bash["hash"] = generated_hash
    input_bash["bash_short_id"] = input_bash["bash_id"][:4] + ":" + generated_hash[:4]

    input_bash["date"] = str(datetime.now())
    if "title" not in input_bash:
        input_bash["title"] = input_bash["bash_short_id"] + " | " + input_bash["date"]

    if "password" in input_bash:
        input_bash["password"] = md5(input_bash["password"].encode()).hexdigest()

    input_bash["stats"] = {
        "used_count": 0,
        "updated_count": 0,
        "up_vote": 0,
        "down_vote": 0
    }
    input_bash["history"] = []

    return input_bash


def validate_before_save(b4, input_bash: dict) -> dict:
    """

    :param b4:
    :param input_bash:
    :return:
    """
    check = b4().validate_input(input_bash)
    # Let's validate the input
    if check[0]:
        b4(input_bash).save()
        del input_bash["_id"]
        result = {
            "status": "success",
            "code": "201",
            "message": "Your bash have been successfully saved to the server,"
                       "\n you can try it by hitting : ./b4.sh {}".format(input_bash["bash_short_id"]),
            "result": input_bash
        }
    else:
        result = {
            "status": "error",
            "code": "400",
            "message": "There are some errors with your inputs, please check the documentation again",
            "error": str(check[1])
        }

    return result


def save_bash(input_bash: dict) -> dict:
    """

    :param input_bash:
    :return:
    """
    # We verify if all required are there
    if "content" in input_bash:
        # we generate the hash of the content
        generated_hash = gen_hash(input_bash["content"])

        # We build our input_bash
        input_bash = build_input_bash(input_bash, generated_hash)

        # We validate before save the bash
        result = validate_before_save(B4, input_bash)
    else:
        result = {
            "status": "error",
            "code": "400",
            "message": "At least, please specify the 'content' of your bash!"
        }

    return result
