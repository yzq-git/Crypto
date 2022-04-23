import telnetlib
from Crypto.Cipher import AES
host = "ctf.nbs.jonbgua.com"
port = 32102
token = '139:MEUCIQCMFjHMkJ2nJMCy/vIvKUxcxTWD4X2lphybXRrhxr4iXAIgf6al3cDqmjr1ZeVCwFyjQDXh7OnFTPo9YqzcUjjm930='
tn=telnetlib.Telnet(host,port)
tn.read_until(b'Please input your token: ')
tn.write(token.encode('ascii')+b'\n')
tag = b"Can you give me the flag please"
#先把tag转换成16进制int类型的list
tag_list=[0x43,0x61,0x6e,0x20,0x79,0x6f,0x75,0x20,0x67,0x69,0x76,0x65,0x20,0x6d,0x65,0x20,0x74,0x68,0x65,0x20,0x66,0x6c,0x61,0x67,0x20,0x70,0x6c,0x65,0x61,0x73,0x65]
instant=[]
ans=[]
def make_cipher(padding_num,trybits): 
    cipher=[]
    for i in range(15-trybits):
        cipher.append(0x00)
    cipher.append(padding_num^(trybits+1))
    if (trybits>0):
        for k in range(trybits):
            cipher.append(instant[16+k-trybits]^(1+trybits))
    for j in range(16):
        cipher.append(0x00)
    return cipher
for i in range(16):
    instant.append(0x00)
tn.read_until(b'The task you choose:')
tn.write(b'1\n')    
for j in range(16):
    for i in range(0x100):
        tn.read_until(b'Ciphertext: ')
        cipher=make_cipher(i,j)
        print(bytes(cipher).hex())
        tn.write(bytes(cipher).hex().encode()+ b'\n')
        reply=tn.read_until(b'Invalid input',0.5).decode()
        print(reply)
        if (reply == 'Invalid input'):
            tn.write(b'1\n')
            continue
        else:
            instant[15-j]=i #DkCn
            tn.write(b'1\n')
            ans = cipher
            break
def make_new_cipher(padding_num):
    ans=[]
    if padding_num==0:
        for i in range(16):
            ans.append(0x10)
        for j in range(16):
            ans[j] = ans[j] ^ instant[j]
        for k in range(16):
            ans.append(0x00)
        return ans
    else:
        for i in range(16 - padding_num):
            ans.append(tag_list[-(16-padding_num)+i])
        for k in range(padding_num):
            ans.append(padding_num)
        for j in range(16):
            ans[j] = ans[j] ^ instant[j]
        for l in range(16):
            ans.append(0x00)
        return ans

for i in range(0x10): #遍历明文最后一分组可能的padding bytes数目
    tn.read_until(b'Ciphertext: ')
    new_cipher = bytes(make_new_cipher(i)).hex()
    tn.write(new_cipher.encode()+ b'\n')
    reply=tn.read_until(b'Nope',0.5).decode()
    print(reply)
    if (reply == 'Nope'):
        tn.write(b'1\n')
        continue
    else:
        break




'''
tn.write(hex(ins_int^0x74686520666c616720706c6561736501)[2:].encode() + b'00'*16 +b'/n')

reply=tn.read_until(b'Invalid input',0.5).decode()
print(reply)
'''