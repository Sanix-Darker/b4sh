from hashlib import sha256, md5


def gen_hash(_str: str) -> str:
    """

    :param _str:
    :return:
    """
    return sha256(_str.encode()).hexdigest()
