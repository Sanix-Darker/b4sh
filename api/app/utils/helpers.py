from hashlib import sha256, md5


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
