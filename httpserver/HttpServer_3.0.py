'''
AID httpServer v3.0
'''
from socket import *
import sys
from threading import Thread
from settings import *

#httpserver 类
class HttpServer(object):
    def __init__(self,address):
        self.address = address
        self.create_socket()
        self.bind(address)
    def create_socket(self):
        self.sockfd =socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    def bind(self,address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(self.address)
    #启动服务器
    def serve_forever(self):
        self.sockfd.listen(2)
        print('listen the port',self.port)
        while True:
            try:
                connfd,addr = self.sockfd.accept()
                print(addr)
            except KeyboardInterrupt:
                print('服务端退出')
                sys.exit(1)
            except Exception as e:
                print(e)
        
            handle_client = Thread(target = self.handle,args =(connfd,))
            handle_client.setDaemon(True)
            handle_client.start()
       

    def handle(self,connfd):
        request = connfd.recv(1024)
        print(request)
        if not request:
            connfd.close()
            return
        request_lines = request.splitlines()
        #获取请求行
        request_line =request_lines[0].decode('utf-8')
        response_body = connect_frame(request_line)
        #发送请求到浏览器
        response_headlers = 'HTTP/1.1 200 OK \r\n'
        response_headlers+='\n'
        response = response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()

def connect_frame(request):
    s = socket()
    try:
        s.connect(frame_addr)
    except Exception as e:
        print('connect to frame error:',e)
        return
    s.send(request.encode())
    response = s.recv(4096*10).decode()
    s.close()
    return response


if __name__=='__main__':
    httpd = HttpServer(ADDR)
    httpd.serve_forever() #启动http服务



