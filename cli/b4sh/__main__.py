from b4sh.module import cmd_parser, list_all
from b4sh import (
    B4SH_DIR,
    VERSION,
    argparse,
    path,
    makedirs
)

if __name__ == "__main__":
    try:
        # Initialize the arguments
        prs = argparse.ArgumentParser()
        prs.add_argument('-c', '--create',
                        help='To create a new B4sh.',
                        type=str)

        prs.add_argument('-g', '--get',
                        help='To get a b4sh by key/id.',
                        type=str)

        prs.add_argument('-f', '--find',
                        help='To find a b4sh by title',
                        type=str)

        prs.add_argument('-ls', '--list',
                        help='To list all available local b4sh shells',
                        action='list',
                        list=list_all())

        prs.add_argument('-v', '--version',
                        action='version',
                        help='To get the actual version of b4sh ',
                        version="b4sh version {}".format(VERSION))

        prs = prs.parse_args()

        cmd_parser(prs)

    except: pass