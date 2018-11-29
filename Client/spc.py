#!/usr/bin/env python3

# imports
import subprocess
import sys
import os
import re
from urllib.parse import urlparse
from coreapi import Client
import requests
import getpass

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
user_details_cond = len(sys.argv) == 3 and sys.argv[1] == 'config' and sys.argv[2] == 'echo'

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


def make_details_dir():
    if not os.path.exists(os.path.expanduser(os.path.join("~", "spc_details"))):
        os.makedirs(os.path.expanduser(os.path.join("~", "spc_details")))


def write_details():
    if not os.path.exists(os.path.expanduser(os.path.join("~", "spc_details"))):
        # need to create auth directory
        make_details_dir()

    with open(os.path.expanduser(os.path.join("~", "spc_details/config.txt")), 'w+') as file:
        for k, v in user_data.items():
            file.write("%s:%s\n" % (k, v))


def read_details():
    if not os.path.exists(os.path.expanduser(os.path.join("~", "spc_details/config.txt"))):
        make_details_dir()
        write_details()
    else:
        with open(os.path.expanduser(os.path.join("~", "spc_details/config.txt")), 'r') as file:
            for row in file:
                data_list = re.split("[:\n]", row)
                user_data[data_list[0]] = data_list[1]


def validated(*args):
    for key in args:
        if user_data[key] == '-':
            return False
        else:
            return True


# The conditions and actions to be taken programmed below

read_details()

# Site Setting for Core API
conn_to_scheme = False
client = Client()
try:
    document = client.get(user_data['site_url'] + 'schema/')
    conn_to_scheme = True
except:
    pass

if server_cond:
    # validate server url
    if os.path.exists(os.path.expanduser(os.path.join("~", "spc_details"))):
        read_details()
        # ip and port
        if validated('site-url'):
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
    print(
        'usage: spc [server set-url <url>] [config edit] [observe <abs-dir-path>] [status] [sync] [--server] [--version] [--help] [en-de list] [en-de update] [en-de update <abs_file_path>]')
    print('For setting url: server set-url <url>')
    print('For setting up username, password, encryption-scheme, encryption-password: config edit')
    print('For displaying username, password, encryption-scheme, encryption-password and other details: config print')
    print('For observing directory given its absolute path: observe <abs-dir-path>')
    print('For getting the status of changed/added/deleted files: status')
    print('For syncing: sync')
    print('For getting server details: --server')
    print('For getting version: --version')
    print('For getting details of all commands: --help')
    print('For getting available Encryption-Decryption schemes: en-de list')
    print('For updating Encryption-Decryption scheme by directly giving details: en-de update')
    print(
        'For updating Encryption-Decryption scheme by giving absolute file path having details: en-de update <abs-file-path>')

elif set_url_cond:
    site_url = sys.argv[3]
    if site_url[-1] == '/':
        pass
    else:
        site_url = site_url + '/'

    site_check_req = requests.get(site_url)
    if site_check_req.ok:
        user_data['site_url'] = site_url
        write_details()
    else:
        print('Invalid URL provided , please try again')

elif user_details_cond:
    censored_data = user_data
    censored_data['password'] = "You can't see me"
    censored_data['encryption_password'] = "You can't see me"
    del censored_data['user_id']
    del censored_data['observed_dir_id']
    for k, v in censored_data.items():
        print("%s : %s\n" % (k, v))

elif observe_path_cond:
    # validate username password scheme user pass and server url
    if os.path.exists(os.path.expanduser(sys.argv[2])) and os.path.isdir(os.path.expanduser(sys.argv[2])):
        user_data['observed_dir'] = sys.argv[2]
        # add to get pk of observed dir
        # add a request to the observed dir
        write_details()
    else:
        print("Error: Directory doesn't exist")

elif login_cond:
    # validate site-url
    user = input('Username: ')
    pas = getpass.getpass(prompt='Password: ', stream=None)
    cpas = getpass.getpass(prompt='Confirm Password: ', stream=None)
    if pas == cpas:
        enc_type = input(f'Encryption Type {schemes}:')
        if enc_type not in schemes:
            print('Error: Incorrect Encryption-Decryption Scheme')
        else:
            enc_pas = getpass.getpass(prompt='Encryption Password: ', stream=None)
            # write request check for correct login
            # write request to get user id
            user_data['username'] = user
            user_data['password'] = pas
            user_data['encryption_scheme'] = enc_type
            user_data['encryption_password'] = enc_pas
            # add user_id here
            write_details()
    else:
        print('The passwords did not match, please try again')

else:
    print("spc: invalid option -- ", end='')
    for i in range(len(sys.argv) - 2):
        print(sys.argv[i + 1] + " ", end='')
    print(sys.argv[len(sys.argv) - 1])
    print("See spc help for more information")
