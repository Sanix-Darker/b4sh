# b4sh

Create, Use and share bash commands easily.

## Requirements

- python (3.x recommend)

## How to install

```shell
pip3 install b4sh
```

## How to use

- To get a b4sh

- To create a custom list of bash commands :

```shell
# To create a custom b4sh
$ b4sh -c 
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


# To create a custom b4sh command from a file
$ b4sh -c script.sh
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

# The create command will create a json file in /home/$USER/.b4sh or C:/b4sh on windows
-rw-r--r-- 1 d4rk3r d4rk3r  46 Dec  8 15:20 conf.json
-rw-r--r-- 1 d4rk3r d4rk3r 425 Dec  8 15:21 hello_world_e48ec.json
```

## Author

- [Sanix-darker](https://github.com/sanix-darker)
