#!/usr/bin/env python3

# imports
import subprocess
import sys
import os
import re
from urllib.parse import urlparse
from coreapi import Client

# Conditions required for arguments

login_cond = len(sys.argv) == 3 and sys.argv[1] == "config" and sys.argv[2] == "edit"
observe_path_cond = len(sys.argv) == 3 and sys.argv[1] == "observe"
sync_dir_cond = len(sys.argv) == 2 and sys.argv[1] == "sync"
set_url_cond = len(sys.argv) == 4 and sys.argv[1] == 'server' and sys.argv[2] == 'set-url'
server_cond = len(sys.argv) == 2 and sys.argv[1] == '--server'
version_cond = len(sys.argv) == 2 and sys.argv[1] == '--version'
en_de_list_cond = len(sys.argv) == 3 and sys.argv[1] == 'en-de' and sys.argv[2] == 'list'
help_cond = len(sys.argv) == 2 and sys.argv[1] == '--help'
status_cond = len(sys.argv) == 2 and sys.argv[1] == 'status'
en_de_update_cond = len(sys.argv) == 3 and sys.argv[1] == 'en-de' and sys.argv[2] == 'update'
en_de_update_file_cond = len(sys.argv) == 4 and sys.argv[1] == 'en-de' and sys.argv[2] == 'update'


# Setting up functions for different tasks

user_data = {'username': '-',
             'password': '-',
             'user_id': '-',
             'encryption_scheme': '-',
             'encryption_password': '-',
             'observed_dir': '-',
             'observed_dir_id': '-',
             'site_url': '-', }
schemes = ['AES', 'BLOFish', 'RSA', 'RC4']
auth_dir_exist_cond = os.path.exists(os.path.expanduser(os.path.join("~", "spc_details")))


def make_details_dir():
    if not auth_dir_exist_cond:
        os.makedirs(os.path.expanduser(os.path.join("~", "spc_details")))


def write_details():
    if not auth_dir_exist_cond:
        # need to create auth directory
        make_details_dir()

    with open(os.path.expanduser(os.path.join("~", "spc_details/config.txt")), 'w+') as file:
        for key, value in user_data.items():
            file.write("%s:%s\n" % (key, value))


def read_details():
    if not auth_dir_exist_cond:
        print("You haven't set up the Server URL yet!")
        print("Run spc server set-url <url>")
        return False
    else:
        with open(os.path.expanduser(os.path.join("~", "spc_details/config.txt")), 'r') as file:
            for row in file:
                data_list = re.split("[:\n]", row)
                user_data[data_list[0]] = data_list[1]


if server_cond:
    # Prints Server Details
    if auth_dir_exist_cond:
        read_details()
        # ip and port
        if not user_data['site_url'] == '-':
            parsed = urlparse(user_data['site_url'])
            print('IP: ' + str(parsed.hostname))
            print('Port: ' + str(parsed.port))
        else:
            print('Error: spc server set-url <url> command needs to be run to know server IP and Port')
    else:
        print('Error: spc server set-url <url> command needs to be run to know server IP and Port')

elif version_cond:
    print('2.0')

elif en_de_list_cond:
    print('Currently available Encryption Schemes are :')
    for s in schemes:
        print(s)

elif help_cond:
    print('usage: spc [server set-url <url>] [config edit] [observe <abs-dir-path>] [status] [sync] [--server] [--version] [--help] [en-de list] [en-de update] [en-de update <abs_file_path>]')
    print('For setting url: server set-url <url>')
    print('For remembering username, password, encryption-scheme, encryption-password: config edit')
    print('For observing directory given its absolute path: observe <abs-dir-path>')
    print('For getting the status of changed/added/deleted files: status')
    print('For syncing: sync')
    print('For getting server details: --server')
    print('For getting version: --version')
    print('For getting details of all commands: --help')
    print('For getting available Encryption-Decryption schemes: en-de list')
    print('For updating Encryption-Decryption scheme by directly giving details: en-de update')
    print('For updating Encryption-Decryption scheme by giving absolute file path having details: en-de update <abs-file-path>')



