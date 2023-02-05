#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    printf "\033[0;33m[-] \033[0;37mThis script must be run as root" 
    exit 1
fi

main() {
    printf "\n\033[0;34m[*] \033[0;37mInstalling...\n"
    apt-get install -y osslsigncode python3 python3-pip wine
    pip install -r requirements.txt
    chmod +x wolfy.py
    wget https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe
    wine python-3.7.9-amd64.exe
    wine "$(which python.exe)" -m pip install pycryptodome pyinstaller tinyaes colorama Cython
    printf '\n\033[0;32m[+] \033[0;37mInstallation completed!'
}

main
