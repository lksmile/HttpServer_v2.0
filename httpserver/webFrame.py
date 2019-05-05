#coding = utf-8
'''
模拟网站后端处理程序
'''
from socket import *
import sys
from select import *
from views import *
frame_ip = '127.0.0.1'
frame_port = 8080
#静态网页位置
staic_dir = './static'
#url决定可以处理什么样子的数据请求
urls =[
    ('/time',show_time),
    ('/hello',say_hello),
    ('/bye',say_bye)
]
if len(sys.argv)<3:
    pass
else:
    frame_ip = sys.argv[1]
    frame_port = int(sys.argv[2])
frame_addr = (frame_ip,frame_port)

class Application(object):
    def __init__(self,frame_addr):
        self.addr = frame_addr
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.addr)
        self.rlist = [self.sockfd]
        self.wlist = []
        self.xlist = []

    def runserver(self):
        self.sockfd.listen(2)
        print('listen the port..',frame_addr[1])
        
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            print('才总')
            for r in rs:
                if r is self.sockfd:
                    connfd,addr = r.accept()
                    self.rlist.append(connfd)
                else:
                    request = r.recv(1024).decode()
                    self.handle(r,request)

    def handle(self,connfd,request):
        #connfd.send(b'hello')
        method = request.split(' ')[0]
        path_info = request.split(' ')[1]

        if method == 'GET':
            if path_info == '/' or path_info[-5:] == '.html':
                response = self.get_html(path_info)
            else:
                response = self.get_data(path_info)
        elif method == 'POST':
            pass
        connfd.send(response.encode())
        connfd.close()
        self.rlist.remove(connfd)
    
    def get_html(self,path_info):
        if path_info == '/':
            get_file = staic_dir+'/index.html'
        else:
            get_file = staic_dir+path_info
        try:
            fd = open(get_file)
        except IOError:
            response = '404'
        else:
            response = fd.read()
        finally:
            return response

    def get_data(self,path_info):
        for url,func in urls:
            if path_info == url:
                response = func()
                break
            else:
                response = '404'
        return response

if __name__=='__main__':
    app =  Application(frame_addr)
    app.runserver()
