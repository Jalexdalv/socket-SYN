import socket

# udpSock = socket.socket(AD_INET,SOCK_DGRAM,protocol=0)

Host = '127.0.0.1'
Port = 9999
Buf_Size = 1024
Addr = (Host,Port)

udpSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpSock.bind(Addr)

while True:
    print('正在接受客户端数据...')
    data, Addr = udpSock.recvfrom(Buf_Size)
    print('服务端接受到数据:',str(data,encoding='utf-8'))
    udpSock.sendto(bytes(str(data,encoding='utf-8'),encoding='utf-8'),Addr)
udpSock.close()