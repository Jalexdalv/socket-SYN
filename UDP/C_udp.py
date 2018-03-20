import socket

Host = '127.0.0.1'
Port = 9999
Buf_Size = 1024
Addr = (Host,Port)

udpClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpClient.connect(Addr)

while True:
    data = input('>>>')
    if not data:
        break
    udpClient.sendto(bytes(data,encoding='utf-8'),Addr)
    data, Addr = udpClient.recvfrom(Buf_Size)
    if not data:
        break
    print('客户端接收到反馈数据:'+str(data,encoding='utf-8'))
udpClient.close()



