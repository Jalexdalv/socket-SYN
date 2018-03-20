import socket

Host = '127.0.0.1'
Port = 8888
Buf_Size = 1024
Addr = (Host,Port)

tcpSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpSock.bind(Addr)
tcpSock.listen(5)

while True:
    print('正在等待客户端连接到服务器...')
    tcpCliSock ,Addr= tcpSock.accept()
    print('...客户端已经连接到服务器:',Addr)

    while True:
        data = tcpCliSock.recv(Buf_Size)
        if not data:
            break
        print('服务端接受到数据:',str(data,encoding='utf-8'))
        tcpCliSock.send(bytes(str(data,encoding='utf-8'),encoding='utf-8'))
    tcpCliSock.close()
tcpSock.close()