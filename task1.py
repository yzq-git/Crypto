import telnetlib
from Crypto.Cipher import AES
host = "ctf.nbs.jonbgua.com"
port = 32102
token = '139:MEUCIQCMFjHMkJ2nJMCy/vIvKUxcxTWD4X2lphybXRrhxr4iXAIgf6al3cDqmjr1ZeVCwFyjQDXh7OnFTPo9YqzcUjjm930='
tn=telnetlib.Telnet(host,port)
tn.read_until(b'Please input your token: ')
tn.write(token.encode('ascii')+b'\n')

def make_cipher(padding_num): 
    cipher=[]
    for i in range(15):
        cipher.append(0x00)
    cipher.append(padding_num^0x01)
    for j in range(15):
        cipher.append(0x00)
    cipher.append(0x00)
    return bytes(cipher).hex()

for i in range(0x100):
        tn.read_until(b'The task you choose:')
        tn.write(b'0\n')
        tn.read_until(b'Ciphertext: ')
        cipher=make_cipher(i)
        print(cipher)
        tn.write(cipher.encode()+ b'\n')
        reply=tn.read_until(b'Invalid input',0.5).decode()
        print(reply)
        if (reply == 'Invalid input'):
            continue
        else:
            break
