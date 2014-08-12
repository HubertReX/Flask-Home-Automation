# -*- coding: utf-8 -*-
import os, sys, urllib2
from time import sleep
import socket

def send_upnp():
    print "start"
    opmsg = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:ProcessInputEvent xmlns:u="urn:adbglobal.com:service:X_ADB_RemoteControl:1">
         <InputEvent>ev=keydn,code=113</InputEvent>
      </u:ProcessInputEvent>
   </s:Body>
</s:Envelope>"""
    open_ports = urllib2.Request("http://192.168.1.105:8080/upnpfun/ctrl/uuid_18d848f0-1dd2-11b2-bf00-000391e19ead/04", opmsg);
    open_ports.add_header("SOAPACTION", '"urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent"');
    open_ports.add_header('Content-type', 'application/xml');
    open_res = urllib2.urlopen(open_ports).read();
    print open_res

    opmsg = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:ProcessInputEvent xmlns:u="urn:adbglobal.com:service:X_ADB_RemoteControl:1">
         <InputEvent>ev=keyup,code=113</InputEvent>
      </u:ProcessInputEvent>
   </s:Body>
</s:Envelope>"""
    open_ports = urllib2.Request("http://192.168.1.105:8080/upnpfun/ctrl/uuid_18d848f0-1dd2-11b2-bf00-000391e19ead/04", opmsg);
    open_ports.add_header("SOAPACTION", '"urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent"');
    open_ports.add_header('Content-type', 'application/xml');
    open_res = urllib2.urlopen(open_ports).read();
    print open_res
    print "end"

def send_key(key, uuid):
  if (key>1000): 
    length = 341 
  elif (key>100):
    length = 340 
  elif (key>10):
    length = 339 
  else:
    length = 338
  
  header = """POST /upnpfun/ctrl/uuid_18d848f0-1dd2-11b2-bf00-000391e19ead/04 HTTP/1.1
HOST: %s:%d
SOAPACTION: "urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent"
CONTENT-TYPE: text/xml; charset="utf-8"
Content-Length: %s

"""
  msg = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:ProcessInputEvent xmlns:u="urn:adbglobal.com:service:X_ADB_RemoteControl:1">
         <InputEvent>ev=%s,code=%d</InputEvent>
      </u:ProcessInputEvent>
   </s:Body>
</s:Envelope>"""

  m1 = """POST /upnpfun/ctrl/uuid_18d848f0-1dd2-11b2-bf00-000391e19ead/04 HTTP/1.1
HOST: 192.168.1.105:8080
SOAPACTION: "urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent"
CONTENT-TYPE: text/xml; charset="utf-8"
Content-Length: 376

<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:ProcessInputEvent xmlns:u="urn:adbglobal.com:service:X_ADB_RemoteControl:1">
         <InputEvent>ev=keydn,code=116</InputEvent>
      </u:ProcessInputEvent>
   </s:Body>
</s:Envelope>"""
  m2 = """POST /upnpfun/ctrl/uuid_18d848f0-1dd2-11b2-bf00-000391e19ead/04 HTTP/1.1
HOST: 192.168.1.105:8080
SOAPACTION: "urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent"
CONTENT-TYPE: text/xml; charset="utf-8"
Content-Length: 376

<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:ProcessInputEvent xmlns:u="urn:adbglobal.com:service:X_ADB_RemoteControl:1">
         <InputEvent>ev=keyup,code=116</InputEvent>
      </u:ProcessInputEvent>
   </s:Body>
</s:Envelope>"""

  length = str(length + 1)
  HOST = "192.168.1.105"
  PORT = 8080

  tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  tcpSocket.connect((HOST, PORT))
#  tcpSocket.sendall('Hello, world')

  m = msg % ("keydn",key)
  h = header % (HOST, PORT, 377)
  print h
  print m
  print len(m)

  tcpSocket.sendall(m1)
  tcpSocket.sendall(m2)
  #tcpSocket.sendall(h)
  #tcpSocket.sendall(m)
  print "#######################################################"
  m = msg % ("keyup",key)
  h = header % (HOST, PORT, 377)
  print h
  print m
  print len(m)
  #tcpSocket.sendall(h)
  #tcpSocket.sendall(m)

#  tcpSocket.send("POST /upnpfun/ctrl/uuid_" + uuid + "/04 HTTP/1.1\n"); 
# tcpSocket.send("Content-Length: " + length + "\n"); 
# tcpSocket.send("Content-Type: text/xml; charset=\"utf-8\"\n"); 
# tcpSocket.send("HOST: "+HOST+":8080\n"); 
# tcpSocket.send("SOAPACTION: \"urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent\"\n"); 
# tcpSocket.send("User-Agent: Fibaro/internal UPnP/1.0 BH-upnpcp/2.0 DLNADOC/1.50\n"); 
# tcpSocket.send("\n"); 
# tcpSocket.send("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"); 
# tcpSocket.send("<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">\n"); 
# tcpSocket.send("<s:Body>\n"); 
# tcpSocket.send("<u:ProcessInputEvent xmlns:u=\"urn:adbglobal.com:service:X_ADB_RemoteControl:1\"><InputEvent>ev=keydn,code=" + str(key) + "</InputEvent></u:ProcessInputEvent></s:Body>\n"); 
# tcpSocket.send("</s:Envelope>\n"); 
# tcpSocket.send("POST /upnpfun/ctrl/uuid_********-1dd2-11b2-a94c-000391******/04 HTTP/1.1\n"); 
# tcpSocket.send("Content-Length: " + length + "\n"); 
# tcpSocket.send("Content-Type: text/xml; charset=\"utf-8\"\n"); 
# tcpSocket.send("HOST: "+HOST+":8080\n"); 
# tcpSocket.send("SOAPACTION: \"urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent\"\n"); 
# tcpSocket.send("User-Agent: Fibaro/internal UPnP/1.0 BH-upnpcp/2.0 DLNADOC/1.50\n"); 
# tcpSocket.send("\n"); 
# tcpSocket.send("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"); 
# tcpSocket.send("<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">\n"); 
# tcpSocket.send("<s:Body>\n"); 
# tcpSocket.send("<u:ProcessInputEvent xmlns:u=\"urn:adbglobal.com:service:X_ADB_RemoteControl:1\"><InputEvent>ev=keyup,code=" + str(key) + "</InputEvent></u:ProcessInputEvent></s:Body>\n"); 
# tcpSocket.send("</s:Envelope>\n"); 

  data = tcpSocket.recv(1024)
  tcpSocket.close()

  print 'Received', repr(data)
  
def main():
  uuid="18d848f0-1dd2-11b2-bf00-000391e19ead"
  #send_key(116, uuid)
  send_upnp()
  
if __name__ == "__main__":
    main()
