from os import getuid
from sys import platform
from pathlib import Path
import pwd


B4SH_DIR = str(Path.home()) + "/" + ".b4sh"
print(B4SH_DIR)
VERSION = "0.1.0"
HOST = "https://b4sh.co/api"
# HOST = "http://127.0.0.1:4352/api"
