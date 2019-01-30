from socket import *
import time,sys
from threading import Thread

'''
    HTTP Server v2.0
    多线程并发
    可以做request请求
    能够返回简单的数据
    类封装
'''
class HTTPServer(object):
    def __init__(self,addr,static_dir):
        self.server_address = addr
        self.static_dir = static_dir
        self.ip = addr[0]
        self.port = addr[1]
        #创建套接字
        self.create_socket()
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.server_address)
    def serve_forever(self):
        self.sockfd.listen(3)
        print('listen to the port %d'%self.port)
        while True:
            try:
                print('hello')
                connfd,addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception as e:
                print('error:',e)
                continue
            clientThread = Thread(target =self.handle,args =(connfd,))
            clientThread.setDaemon(True)
            clientThread.start()
   
    def handle(self,connfd):
        #结束http请求
        request = connfd.recv(1024)
        if not request:
            connfd.close()
            return
        #按行切割
        request_lines =request.splitlines()
        print(connfd.getpeername(),':',request_lines[0])
        getRequest = str(request_lines[0]).split(' ')[1]
        if  getRequest == '/' or getRequest[-5:]=='.html':
            self.get_html(connfd,getRequest)
        else:
            self.get_data(connfd,getRequest)

    def get_html(self,connfd,getRequest):
        if getRequest=='/':
            
            filename = self.static_dir+'/index.html'
        else:
            filename = self.static_dir+getRequest
        try:
            f= open(filename,'rb')
        except Exception:
            responseHeaders = 'HTTP/1.1 404 Not found\r\n'
            responseHeaders+='\r\n'
            responsebody='<h1>Sorry,not found the page</h1>'
        else:
            responseHeaders = 'HTTP/1.1 200 OK\r\n'
            responseHeaders+='\r\n'
            print('正在查找相关内容...')
            responsebody=f.read()
                
                   
              
        finally:
            print('正在发送中')
            response = responseHeaders+responsebody
            connfd.send(response.encode())
            f.close()
    def get_data(self,connfd,getRequest):
        urls = ['/time','/tedu','/hello']
        if getRequest in urls:
            responseHeaders = 'HTTP/1.1 200 OK\r\n'
            responseHeaders+='\r\n'
            if getRequest == '/time':
                import time 
                responsebody = time.ctime()
            elif getRequest == '/tedu':
                responsebody = '帅哥'
            elif getRequest == '/hello':
                responsebody = 'faghalgha'
            else:
                responseHeaders = 'HTTP/1.1 404 Not found\r\n'
                responseHeaders = '\r\n'
                responsebody = 'SOrry not data'
            print('正在发送中....')
            response = responseHeaders + responsebody
            connfd.send(response.encode())
                



# if __name__=='__main___':
    #用户自己确定
server_addr = ('0.0.0.0',9999)
static_dir = './static'  #存放网页
httpd = HTTPServer(server_addr,static_dir)
#启动http server
httpd.serve_forever()