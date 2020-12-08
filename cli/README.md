# b4sh

Create, Use and share bash commands easily.

## Requirements

- python (3.x recommend)

## How to install

```shell
pip3 install b4sh
```

## How to use

```shell script
$ b4sh -h
[x] Starting b4sh...

usage: b4sh [-h] [-g GET] [-f FIND] [-c CREATE] [-ls LIST] [-v]

optional arguments:
  -h,  --help    Show this help message and exit.

  -g,  --get     To get a b4sh by key/id, Ex: b4sh -g apache2_eerft.

  -f,  --find    To find a b4sh by name online, Ex: b4sh -f nginx.

  -r,  --run     To run directly with the good key/id, Ex: b4sh -r nginx_eedrf4.

  -c,  --create  To create a new B4sh, Ex: b4sh -c / Or with a file_path, Ex: b4sh -c script.sh

  -ls, --list    To list all available offline/local b4sh shells.

  -v,  --version To get the actual version of b4sh.
```

#### To create a custom list of bash commands :

- To create a custom b4sh

`$ b4sh -c`
``` 
[x] Starting b4sh...
[-] --------------------
[-] author : d4rk3r
[-] os-pid : 15205
[-] --------------------

[+] Creating a new b4sh...

[?] Title : hello world
[?] Description : Just an echo of hello world
[?] Content** ( In a new line, Ctrl-D to save the content ): 
echo 'Hello World !'
[+] b4sh hello_world_e48ec created/saved successfully !
```

- To create a custom b4sh command from a file

`$ b4sh -c script.sh`

```
[x] Starting b4sh...
[-] --------------------
[-] author : d4rk3r
[-] os-pid : 11205
[-] --------------------

[+] Creating a new b4sh...

[?] Title : script.sh
[?] Description : Just a bash script
[+] Getting the content...
[+] b4sh script.sh_b3155 created/saved successfully !
```

The `create` command will create a json file in `/home/$USER/.b4sh` or `C:/b4sh` on Windows
```
-rw-r--r-- 1 d4rk3r d4rk3r  46 Dec  8 15:20 conf.json
-rw-r--r-- 1 d4rk3r d4rk3r 425 Dec  8 15:21 hello_world_e48ec.json
```

#### To search for a b4sh :

You just have to use the parameter `find`.

`b4sh -f hello`
```
[x] Starting b4sh...
[-] Searching for : hello...
[+] Listing results (1) :
[-] 1-) hello_world_e48ec

[?] Your choice (0 to quit):1
[-] Checking offline : hello_world_e48ec...
[-] Getting : hello_world_e48ec...
[-] - - -
[-] > hello_world_e48ec
[-] > sha256: bf0473c2d30f6f7bda45508eebe0483ec9b99fc298ed5d7e105a7eacd2fafcb3
[?] > See the content ? (Y/N): y
echo 'Hello World !'

[?] > See stats (used, votes...) ? (Y/N): y
[=] Stats:
[=] ____used_count: 0
[=] ____updated_count: 0
[=] ____up_vote: 0
[=] ____down_vote: 0
[?] > Execute it ? (Y/N): y
Hello World !
```

- To get a b4sh by key/id :

`b4sh -g hello_world_e48ec`
```
[x] Starting b4sh...
[-] Checking offline : hello_world_e48ec...
[-] Getting : hello_world_e48ec...
[-] - - -
[-] > hello_world_e48ec
[-] > sha256: bf0473c2d30f6f7bda45508eebe0483ec9b99fc298ed5d7e105a7eacd2fafcb3
[?] > See the content ? (Y/N): y
echo 'Hello World !'

[?] > See stats (used, votes...) ? (Y/N): y
[=] Stats:
[=] ____used_count: 0
[=] ____updated_count: 0
[=] ____up_vote: 0
[=] ____down_vote: 0
[?] > Execute it ? (Y/N): y
Hello World !
```

- To run by key/id :

`b4sh -r hello_world_e48ec`
```
[x] Starting b4sh...
[-] Checking offline : hello_world_e48ec...
[-] Getting : hello_world_e48ec...
[-] - - -
[?] > Execute it ? (Y/N): y
Hello World !
```

- To list all offline b4sh :

`b4sh -ls`
```
[x] Starting b4sh...
[+] Listing results (1) :
[-] 1-) hello_world_e48ec

[?] Your choice (0 to quit):0
[x] Stopping b4sh.
```

## Author

- [Sanix-darker](https://github.com/sanix-darker)
