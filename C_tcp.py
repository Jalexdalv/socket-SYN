import socket

Host = '127.0.0.1'
Port = 8888
Buf_Size = 1024
Addr = (Host,Port)

tcpClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpClient.connect(Addr)

while True:
    data = input('>>>')
    if not data:
        break
    tcpClient.send(bytes(data,encoding='utf-8'))
    data = tcpClient.recv(Buf_Size)
    if not data:
        break
    print('客户端接收到反馈数据:'+str(data,encoding='utf-8'))
tcpClient.close()



