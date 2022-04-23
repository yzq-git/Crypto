from Crypto.Cipher import AES
import os

flag = open("flag").read()
flag1 = flag2 = flag

key = os.urandom(16)


def pad(msg):
    n = AES.block_size - len(msg) % AES.block_size
    return msg + bytes([n]) * n


tag = b"Can you give me the flag please"


def unpad(msg):
    assert len(msg) > 0 and len(msg) % AES.block_size == 0
    n = msg[-1]
    assert 1 <= n <= AES.block_size
    assert msg[-n:] == bytes([n]) * n
    return msg[:-n]


while True:
    try:
        k = int(input("The task you choose:"))
        ciphertext = bytes.fromhex(input("Ciphertext: "))
        aes = AES.new(key, AES.MODE_CBC, ciphertext[: AES.block_size])
        plaintext = unpad(aes.decrypt(ciphertext[AES.block_size:]))
        if k==0:
            if pad(plaintext)[-1] == pad(tag)[-1]:
                print(flag1)
            else:
                print("Nope")
        elif k==1:
            if pad(plaintext)[-AES.block_size:] == pad(tag)[-AES.block_size:]:
                print(flag2)
            else:
                print("Nope")
        elif k==2:
            if plaintext == tag:
                print(flag)
            else:
                print("Nope")
    except:
        print("Invalid input")