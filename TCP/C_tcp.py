import socket,re,os

REGEX_DOWNFILE = '^downfile\:([\w\W]*)'
REGEX_UPFILE = '^upfile\:([\w\W]*)'
REGEX_MSG = '^msg\:([\w\W]*)'
PATH_DOWN = 'F:/TCPdownload'

def check_file(path):
    if os.path.exists(path):
        return True
    else:
        return False

def upload_file(data,tcpClient):
    upfile_data = re.match(REGEX_UPFILE,data).group(1).strip()
    regex_filename = '^.*[/\\\//]([\w\W]*)$'
    filename = re.match(regex_filename,upfile_data).group(1).strip()
    if check_file(upfile_data):
        with open(upfile_data, 'rb') as f:
            UP_FILE = f.read()
        tcpClient.send(UP_FILE)
        tcpClient.send(bytes(filename,encoding='utf-8'))
    else:
        tcpClient.send(bytes('该路径下此文件不存在！',encoding='utf-8'))

def download_file(data,tcpClient):
    filedata = data
    reve_data = tcpClient.recv(Buf_Size)
    filename = reve_data
    f = open(PATH_DOWN+'/'+str(filename,encoding='utf-8'),'w')
    f.write(str(filedata,encoding='gb2312'))
    print('从服务器下载文件完成！')

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

tcpClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#连接服务端
tcpClient.connect(Addr)
#接受欢迎消息
print(str(tcpClient.recv(Buf_Size),encoding='utf-8'))

while True:
    data = input('>>>')
    if not data:
        break
    tcpClient.send(bytes(data,encoding='utf-8'))
    
    #分析数据
    if command_paser(data)==1:
        reve_data = tcpClient.recv(Buf_Size)
        if not reve_data:
            break
        print(str(reve_data,encoding='utf-8'))
    elif command_paser(data)==2:
        upload_file(data,tcpClient)
        print(str(tcpClient.recv(Buf_Size),encoding='utf-8'))
    elif command_paser(data)==3:
        reve_data = tcpClient.recv(Buf_Size)
        if not reve_data:
            break
        download_file(reve_data,tcpClient)
        tcpClient.send(bytes('客户端下载文件完成',encoding='utf-8'))
    else:
        reve_data = tcpClient.recv(Buf_Size)
        if not reve_data:
            break
        print(str(reve_data,encoding='utf-8'))
tcpClient.close()



