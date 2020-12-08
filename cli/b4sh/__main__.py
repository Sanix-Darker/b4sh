from b4sh.module import cmd_parser, list_all, create_b4sh, paste_help
from b4sh import (
    B4SH_DIR,
    VERSION,
    argparse,
    path,
    makedirs
)
from sys import argv

if __name__ == "__main__":

    if len(argv) > 1:
        if "-ls" in argv[1] or "--list" in argv[1]:
            print("[x] Starting b4sh...")
            list_all()
        elif '-c' in argv[1] or '--create' in argv[1]:
            print("[x] Starting b4sh...")
            if len(argv) > 2:
                create_b4sh(argv[2])
            else:
                create_b4sh()
        elif '-h' in argv[1] or '--help' in argv[1]:
            print("[x] Starting b4sh...")
            paste_help()
        else:
            print("[x] Starting b4sh...")
            # Initialize the arguments
            prs = argparse.ArgumentParser('b4sh', add_help=False)

            prs.add_argument('-g', '--get',
                             help='To get a b4sh by key/id, Ex: b4sh -g apache2_eerft',
                             type=str)

            prs.add_argument('-f', '--find',
                             help='To find a b4sh by name online, Ex: b4sh -f nginx',
                             type=str)

            prs.add_argument('-v', '--version',
                             action='version',
                             help='To get the actual version of b4sh, Ex: b4sh -v',
                             version="[-] b4sh version {}".format(VERSION))

            prs = prs.parse_args()

            cmd_parser(prs)
    else:
        paste_help()
