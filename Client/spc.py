#!/usr/bin/env python3

# imports
import subprocess
import sys
import os
import re
from urllib.parse import urlparse
import coreapi
import requests
import getpass
from datetime import datetime
from pathlib import Path

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
            file.write("%s|%s\n" % (k, v))


def read_details():
    if not os.path.exists(os.path.expanduser(os.path.join("~", "spc_details/config.txt"))):
        make_details_dir()
        write_details()
    else:
        with open(os.path.expanduser(os.path.join("~", "spc_details/config.txt")), 'r') as file:
            for row in file:
                data_list = re.split("[|\n]", row)
                user_data[data_list[0]] = data_list[1]


def validated(*args):
    for key in args:
        if user_data[key] == '-':
            return False
        else:
            return True


def command_run(bash_command):
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (temp_list, err) = process.communicate()
    temp_list = temp_list.decode().split('\n')
    temp_list = list(filter(None, temp_list))
    return temp_list


def get_client_files(dir_name):
    bash_name_command = "find " + dir_name + " -exec basename {} ;"
    bash_path_command = "find " + dir_name
    bash_b2_command = "find " + dir_name + " -exec b2sum {} ;"
    bash_date_command = "find " + dir_name + " -exec date -r {} +%FT%T.%6N%z ;"
    bash_type_command = "find " + dir_name + " -exec file -b --mime-type {} ;"

    name_list = command_run(bash_name_command)
    path_list = command_run(bash_path_command)
    b2_list = command_run(bash_b2_command)
    date_list = command_run(bash_date_command)
    type_list = command_run(bash_type_command)

    temp = b2_list[:]
    temp_keys = []
    temp_values = []
    b2_list.clear()
    for t in temp:
        temp_data = t.split('  ', 1)
        temp_keys.append(temp_data[1])
        temp_values.append(temp_data[0])
    b2_list = dict(zip(temp_keys, temp_values))

    func_client_files = []
    for i in range(0, len(path_list)):
        dict_obj = {'file_path': path_list[i], 'file_type': type_list[i], 'modified_time': date_list[i], 'name': name_list[i]}
        if path_list[i] in b2_list:
            dict_obj['b2code'] = b2_list[path_list[i]]
        else:
            dict_obj['b2code'] = '-'
        func_client_files.append(dict_obj)

    return func_client_files


def get_status():
    server_files = client.action(document, ['user', 'status', 'read'],
                                 params={'username': user_data['username'],
                                         'dir_path': user_data['observed_dir']})
    server_files = [dict(s) for s in server_files]
    for s in server_files:
        d = s['modified_time']
        if ":" == d[-3:-2]:
            d = d[:-3] + d[-2:]
        s['modified_time'] = datetime.strptime(s['modified_time'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%c')
        s['file_path'] = s['file_path'][:-1]

    client_files = get_client_files(dir_name=user_data['observed_dir'])
    base_name = os.path.basename(Path(user_data['observed_dir']))
    for c in client_files:
        c['modified_time'] = datetime.strptime(c['modified_time'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%c')
        c['file_path'] = base_name + '/' + c['file_path'][len(user_data['observed_dir']):]

    status_diff_content = []
    status_in_both = []
    client_dict = {cf['file_path']: cf for cf in client_files}
    server_dict = {cf['file_path']: cf for cf in server_files}
    status_client_only = list(set(client_dict.keys()) - set(server_dict.keys()))
    status_server_only = list(set(server_dict.keys()) - set(client_dict.keys()))
    in_both_keys = list(set(server_dict.keys()) & set(client_dict.keys()))
    for b_key in in_both_keys:
        if client_dict[b_key]['b2code'] == server_dict[b_key]['b2code']:
            status_in_both.append(b_key)
        else:
            status_diff_content.append(b_key)
    status_client_only.sort(key=len)
    status_server_only.sort(key=len)
    status_diff_content.sort(key=len)
    status_in_both.sort(key=len)
    return status_client_only, status_server_only, status_diff_content, status_in_both, server_dict, client_dict



# The conditions and actions to be taken programmed below

read_details()
client_dict = {}
server_dict = {}

auth = coreapi.auth.BasicAuthentication(username=user_data['username'], password=user_data['password'])
client = coreapi.Client(auth=auth)

if server_cond:
    # validate server url
    if os.path.exists(os.path.expanduser(os.path.join("~", "spc_details"))):
        read_details()
        # ip and port
        if validated('site_url'):
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
    print('For updating Encryption-Decryption scheme by giving absolute file path having details: en-de update <abs-file-path>')

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
        print('Server was set to the URL : ' + site_url)
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
        print('Currently observing Directory : ' + user_data['observed_dir'])
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
            auth = coreapi.auth.BasicAuthentication(username=user_data['username'], password=user_data['password'])
            client = coreapi.Client(auth=auth)
            try:
                print('Connecting to the site : ' + user_data['site_url'] + 'schema/')
                document = client.get(user_data['site_url'] + 'schema/')
                write_details()
                print('Logged in successfully as ' + user_data['username'] + '. Please select a directory to be observed')
            except coreapi.exceptions.ErrorMessage:
                print('There was an error in logging in ( Invalid account details ). Please try again.')
            except coreapi.exceptions.NetworkError:
                print('There was a network error. Please try again.')
            except:
                print('Some error occured, please try again')

    else:
        print('The passwords did not match, please try again')

elif status_cond:
    # validate url , username, password, observing directory
    try:
        print('Connecting to the site : ' + user_data['site_url'] + 'schema/')
        document = client.get(user_data['site_url'] + 'schema/')
        (status_client_only, status_server_only, status_diff_content, status_in_both, server_dict, client_dict) = get_status()
    except coreapi.exceptions.ErrorMessage:
        print('There was an error in logging in ( Invalid account details ). Please try again.')
    except coreapi.exceptions.NetworkError:
        print('There was a network error. Please try again.')
    except:
        print('Some error occured, please try again')

    print("Files only on Client : ")
    for s in status_client_only:
        print(s)
    print(" ")
    print("Files only on Server : ")
    for s in status_server_only:
        print(s)
    print(" ")
    print("Files which have been modified : ")
    for s in status_diff_content:
        print(s)
    print(" ")
    print("Files same in both : ")
    for s in status_in_both:
        print(s)
    print(" ")

elif sync_dir_cond:
    (status_client_only, status_server_only, status_diff_content, status_in_both, server_dict, client_dict) = get_status()

    # Handling only on Client Files
    if len(status_client_only) > 0:
        print("Files only on Client : ")
        for s in status_client_only:
            print(s)
        print(" ")
        choice_1 = input("Do you want to transfer all of them to server ? (y/n)")
        if choice_1 == 'y':
            for s in status_client_only:
                # call upload to server on client_dict[s]
                print("Uploaded " + s + " to the server.")
            print("Done.\n")
        elif choice_1 == 'n':
            for s in status_client_only:
                print("Do you want to move " + s + " to server, or delete it from client ? (m/d)")
                if client_dict[s]['file_type'] == 'inode/directory':
                    print("If you choose to delete this Directory,")
                    print(" all files inside it will also be deleted from the client")
                choice_2 = input()
                if choice_2 == 'm':
                    # call upload to server on client_dict[s] check if not directory to get filecontent
                    # pass userdata[observed_dir]
                    print("Uploaded " + s + " to the server.")
                elif choice_2 == 'd':
                    # delete data from client
                    print("Deleted " + s + " from client.")
                else:
                    print("Invalid Choice.")
                    sys.exit(2)
            print("Done.\n")
        else:
            print("Invalid choice.")
            sys.exit(2)

    # Handling only on Server Files
    if len(status_server_only) > 0:
        print("Files only on Server : ")
        for s in status_server_only:
            print(s)
        print(" ")
        choice_1 = input("Do you want to download all of them to client ? (y/n)")
        if choice_1 == 'y':
            for s in status_server_only:
                # call download from server for server_dict[s] also check file type
                # pass user_data[observed_dir]
                print("Downloaded " + s + " to the client.")
            print("Done.\n")
        elif choice_1 == 'n':
            for s in status_server_only:
                print("Do you want to copy " + s + " to the client, or delete it from server ? (c/d)")
                if server_dict[s]['file_type'] == 'inode/directory':
                    print("If you choose to delete this Directory,")
                    print(" all files inside it will also be deleted from the server")
                choice_2 = input()
                if choice_2 == 'c':
                    # call download from server for server_dict[s] also check file type
                    # pass user_data[observed_dir]
                    print("Downloaded " + s + " to the client.")
                elif choice_2 == 'd':
                    # delete data from server
                    print("Deleted " + s + " from server.")
                else:
                    print("Invalid Choice.")
                    sys.exit(2)
            print("Done.\n")
        else:
            print("Invalid choice.")
            sys.exit(2)

    # Handling Files that have been edited
    if len(status_diff_content) > 0:
        print("Modified Files : ")
        for s in status_diff_content:
            print(s)
        print(' ')
        print('Do you want to:\n'
              '1.Get all files from Server\n'
              '2.Put all files from Client\n'
              '3.Select for each file\n')
        choice_1 = input()
        if choice_1 == '1':
            for s in status_diff_content:
                # delete the file from client
                # call download from server for server_dict[s]
                print("Downloaded " + s + " from server.")
            print("Done.\n")
        elif choice_1 == '2':
            for s in status_diff_content:
                # call delete from server for server_dict[s]
                # call upload to server for client_dict[s]
                print("Uploaded " + s + " from client.")
            print("Done.\n")
        elif choice_1 == '3':
            for s in status_diff_content:
                print("Do you want to keep the server copy or client copy of " + s + " ? (s/c)")
                if server_dict[s]['file_type'] == 'inode/directory':
                    print("This is a directory, all data from whichever side is deleted will be lost.")
                choice_2 = input()
                if choice_2 == 's':
                    # delete file from client
                    # call download from server
                    print("Downloaded " + s + " from server.")
                elif choice_2 == 'c':
                    # delete file from server
                    # call upload from client
                    print("Uploaded " + s + " from client.")
                else:
                    print("Invalid choice.")
                    sys.exit(2)
            print("Done.\n")

        else:
            print("Invalid choice.")
            sys.exit(2)

else:
    print("spc: invalid option -- ", end='')
    for i in range(len(sys.argv) - 2):
        print(sys.argv[i + 1] + " ", end='')
    print(sys.argv[len(sys.argv) - 1])
    print("See spc help for more information")
