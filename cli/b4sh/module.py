from b4sh.settings import B4SH_DIR

from b4sh.utils import *


def cmd_parser(args: object):
    """

    :param args:
    :return:
    """
    # we check if the b4sh folder exist
    # if not we install it
    if not path.exists(B4SH_DIR):
        makedirs(B4SH_DIR)

    # the get method
    if args.get is not None:
        get(args.get)

    # The find method
    if args.find is not None:
        find(args.find)
