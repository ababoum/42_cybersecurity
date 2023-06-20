#!/usr/bin/env python3

import sys
import copy
import time
from TOTP import TOTP
from hashlib import sha512

arguments = copy.deepcopy(sys.argv[1:])
if len(arguments) == 0:
    print('Usage: ./ft_otp.py -g KEY_FILE or ./ft_otp.py -k ENC_KEY_FILE')
    exit()

file = ''
if arguments[0] == '-g' and len(arguments) == 2:
    file = arguments[1]

elif arguments[0] == '-k' and len(arguments) == 2:
    file = arguments[1]

else:
    print('Usage:')
    print('./ft_otp.py -g KEY_FILE to save a key')
    print('or')
    print('./ft_otp.py -k ENC_KEY_FILE to generate a one-time password')
    exit()

if arguments[0] == '-g':
    try:
        with open(file, 'r') as f:
            key = f.read()
            key_hex = int(key, 16)
    except FileNotFoundError:
        print('Error: file not found.')
        exit()
    except ValueError:
        print('Error: file must contain 64 hexadecimal characters.')
        exit()
    if len(key) != 64:
        print('Error: key must be 64 hexadecimal characters.')
        exit()

    # store the encrypted key in a file
    with open('ft_otp.key', 'w') as f:
        f.write(sha512(key.encode()).hexdigest())
        print("Key successfully generated and stored in ft_otp.key")

elif arguments[0] == '-k':
    totp = TOTP()
    try:
        with open('ft_otp.key', 'r') as f:
            key = f.read()
    except FileNotFoundError:
        print('Error: ft_otp.key not found.')
        exit()

    # generate a one-time password
    print(totp.generateTOTP(key, str(int(time.time()))[-16:]))
