from b4sh.module import cmd_parser
from b4sh import (
    B4SH_DIR,
    argparse,
    path, 
    makedirs
) 


if __name__ == "__main__":
    # Initialize the arguments
    prs = argparse.ArgumentParser()
    prs.add_argument('-c', '--create',
        help='To create a B4sh.',
        type=str)

    prs.add_argument('-g', '--get',
        help='The key/id of the b4sh.',
        type=str)

    prs.add_argument('-f', '--find',
        help='To find a b4sh by text ',
        type=str)

    prs = prs.parse_args()

    # we check if the b4sh folder exist
    if not path.exists(B4SH_DIR):
        makedirs(B4SH_DIR)

    cmd_parser(prs)
