from os import getuid
from sys import platform
import pwd


USERNAME = pwd.getpwuid(getuid())[0]

B4SH_DIR = "C:/.b4sh" if platform == 'Windows' else "/home/{}/.b4sh".format(USERNAME)

HOST = "https://b4sh.co/api"
# HOST = "http://127.0.0.1:4352/api"
