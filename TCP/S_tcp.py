import socket,os,re

REGEX_DOWNFILE = '^downfile\:([\w\W]*)'
REGEX_UPFILE = '^upfile\:([\w\W]*)'
REGEX_MSG = '^msg\:([\w\W]*)'
PATH_UP = 'F:/TCPupload'

def check_file(path):
    if os.path.exists(path):
        return True
    else:
        return False

def download_file(data,tcpCliSock):
    downfile_data = re.match(REGEX_DOWNFILE,data).group(1).strip()
    regex_filename = '^.*[/\\\//]([\w\W]*)$'
    filename = re.match(regex_filename,downfile_data).group(1).strip()
    if check_file(downfile_data):
        with open(downfile_data, 'rb') as f:
            DOWN_FILE = f.read()
        tcpCliSock.send(DOWN_FILE)
        tcpCliSock.send(bytes(filename,encoding='utf-8'))
    else:
        tcpCliSock.send(bytes('该路径下此文件不存在！',encoding='utf-8'))

def upload_file(tcpCliSock):
    data = tcpCliSock.recv(Buf_Size)
    filedata = data
    reve_data = tcpCliSock.recv(Buf_Size)
    filename = reve_data
    f = open(PATH_UP+'/'+str(filename,encoding='utf-8'),'w')
    f.write(str(filedata,encoding='gb2312'))
    print('客户端上传文件完成！')
        
def ex_msg(data,tcpCliSock):
    msg_data = re.match(REGEX_MSG,data).group(1).strip()
    print('服务端收到客户端发来的会话:',msg_data)
    tcpCliSock.send(bytes('客户端已成功向服务端发送会话:'+msg_data,encoding='utf-8'))

def command_paser(data):
    if re.match(REGEX_DOWNFILE,data):
        return 3
    if re.match(REGEX_UPFILE,data):
        return 2
    if re.match(REGEX_MSG,data):
        return 1
    return 0



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
    #向客户端返回欢迎信息
    tcpCliSock.send(bytes('欢迎连接到服务器'+str(Host)+':'+str(Port),encoding='utf-8'))

    while True:
        #接受传输信息
        data = tcpCliSock.recv(Buf_Size)
        if not data:
            break
        print('服务端接收到客户端消息:',str(data,encoding='utf-8'))
        data = str(data,encoding='utf-8')
        #分析数据
        if command_paser(data)==1:
            ex_msg(data,tcpCliSock)
        elif command_paser(data)==2:
            upload_file(tcpCliSock)
            tcpCliSock.send(bytes('客户端上传文件完成',encoding='utf-8'))
        elif command_paser(data)==3:
            download_file(data,tcpCliSock)
        else:
            tcpCliSock.send(bytes('命令错误，请确认后重新输入！',encoding='utf-8'))
    tcpCliSock.close()
tcpSock.close()
