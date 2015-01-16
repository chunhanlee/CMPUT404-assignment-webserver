import SocketServer
import os.path
# coding: utf-8

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
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/ 

#fixing VM time so comits work


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        # parse incoming request
        self.data = self.request.recv(1024).strip()
        Splitdata =  self.data.splitlines()
        Firstword = Splitdata[0].split()
      	
	#variables used
    	style = ""
    	mes = ""
        HTTP200 = "HTTP/1.1 200 OK\n" + "Content-type: text/"
        HTTP2002 ="HTTP/1.1 200 OK" + "Content-type: text/"
        HTTP404 = "HTTP/1.1 404 Not Found\n"+"Content-Type: text/html\n\n"+"<!DOCTYPE html>\n"+"<html><body>HTTP/1.1 404 Not Found\n"+"Not found on server directory</body></html>"
        
        #get pathway requested
        pathway = os.getcwd() + "/www"+ Firstword[1]

        #see if what is being requested is a css or html
        style = pathway.split(".")[-1].lower()
        
        #check if pathway is a file and check if the requested pathway is in what the file returns as its pathway
        if (os.path.isfile(pathway) and os.getcwd() in os.path.realpath(pathway)):
            #check if end is html or css
            if (style == "html" or style == "css"):
                mes = (HTTP200+style+"\n\n"+open(pathway).read())

        #checks for first html file and check if the requested pathway is in what the file returns as its pathway, passes on initial get request
        elif (os.path.isdir(pathway) and os.getcwd() in os.path.realpath(pathway)):
    
            #open index file with format html
            pathway = pathway+"/index.html"
            mes = (HTTP2002+style+"\n\n"+ open(pathway).read())
        
        #redirects the /deep.css to display on page
        elif style == "css":
            pathway = pathway.split(".")[0].lower()
            pathway = pathway + "/deep.css"
            
            mes = (HTTP2002+style+"\n\n"+ open(pathway).read())
        
        #doesnt exist! not in deep or was not www index or was not get request
        else:
            mes = (HTTP404)

        #send response to the client
        self.request.sendall(mes)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
