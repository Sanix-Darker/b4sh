from b4sh import *
from sys import argv

from b4sh.utils.create import create_b4sh


if __name__ == "__main__":

    if len(argv) > 1:
        print("[x] Starting b4sh...")
        if "-ls" in argv[1] or "--list" in argv[1]:
            list_all()
        elif '-c' in argv[1] or '--create' in argv[1]:
            create_b4sh(argv[2]) if len(argv) > 2 else create_b4sh()
        elif '-h' in argv[1] or '--help' in argv[1]:
            paste_help()
        else:
            # Initialize the arguments
            prs = argparse.ArgumentParser('b4sh', add_help=False)
            prs.add_argument('-g', '--get',
                             help='To get a b4sh by key/id, Ex: b4sh -g apache2_eerft',
                             type=str)
            prs.add_argument('-f', '--find',
                             help='To find a b4sh by name online, Ex: b4sh -f nginx',
                             type=str)
            prs.add_argument('-r', '--run',
                             help='To run directly with the good key/id, Ex: b4sh -r nginx_eedrf4',
                             type=str)
            prs.add_argument('-v', '--version',
                             action='version',
                             help='To get the actual version of b4sh, Ex: b4sh -v',
                             version="[-] b4sh version {}".format(VERSION))

            prs = prs.parse_args()
            cmd_parser(prs)
    else:
        paste_help()
