#  coding: utf-8 
import socketserver
import http.server
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#current os path
PATH = os.getcwd() + "/www/"
INDEX = "index.html"

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
      
        if self.data != b'':
            request_method = str(self.data).split(' ')[0]
            request_path = str(self.data).split(' ')[1]
            print(request_method)
            if request_method == "b'GET":
                print(request_path)
                self.response(request_path)
            else:
                self.status_405()


    def response(self,path):     
        try:
            if  os.path.join(PATH, path).endswith('.html') or (os.path.isdir(os.path.join(PATH, path.strip('/'))) and path.endswith('/')):
                
                if os.path.isdir(os.path.join(PATH, path.strip('/'))):
                    path = path + INDEX 
                f = open( os.path.join(PATH, path[1:]), "r")
                data = f.read()
                t = 'html'
                f.close()
                self.status_200(t,data)
            elif os.path.join(PATH, path).endswith('.css'):
                try:
                    f = open( os.path.join(PATH, path[1:]), "r")
                    data = f.read()
                    t = 'css'
                    f.close()
                    self.status_200(t,data)
                except:
                    self.status_404()  
            elif os.path.isdir(os.path.join(PATH, path.strip('/'))) and not path.endswith('/'):
                self.status_301(path)
            else:       
                self.status_404()      
        except Exception as e:
            print(e)
    
    def status_200(self,mimetypes,data):
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n" + 
            "Content-Type: text/"+mimetypes+ "\r\n\r\n"+
            data , 'utf-8'))

    def status_301(self,path):
        print("HTTP/1.1 301 Move Permanently\r\nLocation: http://127.0.0.1:8080"+path +"/\r\nContent-Type: text/html\r\n")
        self.request.sendall(bytearray("HTTP/1.1 301 Move Permanently\r\nRedirected to :"+ path +"/\r\nContent-Type: text/html\r\n\r\n"  , 'utf-8')) 

    def status_404(self):
        #print("here\n")
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n"
         "Content-Type: text/html\r\n\r\n" +
        "<body>\
        <h1>Error response</h1> \
        <p>Error code 404.</p> \
        <p>Message: File not found.</p>\
        </body> ", 'utf-8')) 

    def status_405(self):
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n"
         "Content-Type: text/html\r\n\r\n" +
        "<body>\
        <h1>Error response</h1> \
        <p>Error code 405.</p> \
        <p>Message: Method Not Allowed.</p>\
        </body> ", 'utf-8')) 

        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
