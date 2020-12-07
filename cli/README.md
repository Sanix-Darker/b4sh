# b4sh

Create, Use and share bash commands easily.

## Requirements

- python (3.x recommend)

## How to install

```shell
pip3 install b4sh
```

## How to use

```shell
# To install nginx for example !
b4sh -g nginx_debian_3ee
# This command will run
sudo apt update
sudo apt install nginx
sudo service nginx status

# For a custom command
b4sh -g vim_445te
# This will run :
apt update
apt install wget unzip
echo "[+] Getting vim..."
wget "http://www.vim.org/scripts/download_script.php?src_id=11834" -O vim.zip
echo "[+]  Unzipping the vim zip..."
unzip vim.zip
echo "[+] Deleting the zip"
rm vim.zip
```

## Author

- [Sanix-darker](https://github.com/sanix-darker)
