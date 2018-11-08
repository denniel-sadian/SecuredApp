#! python3
# December 16, 2017

r"""Module for string encryption and decryption.

This module can encrypt and decrypt strings.
"""


def encrypt(string: str) -> str:
    numbers = []
    hexadecimal = ''
    for char in string:
        numbers.append(ord(char))
    for number in numbers:
        hexadecimal += str(hex(number))
    return hexadecimal[::-1]


def decrypt(string: str) -> str:
    hexadecimals = []
    numbers = []
    decrypted = ''
    for not_yet_hexa in string[::-1].split('0x')[1:]:
        hexadecimals.append(f'0x{not_yet_hexa}')
    for hexa in hexadecimals:
        numbers.append(int(hexa, base=16))
    for number in numbers:
        decrypted += f'{chr(number)}'
    return decrypted


if __name__ == '__main__':
    x = 'Denniel Luis Saway Sadian'
    a = encrypt(x)
    b = decrypt(a)
    print(a)
    print(b)
