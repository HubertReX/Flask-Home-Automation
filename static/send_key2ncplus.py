# -*- coding: utf-8 -*-
import os, sys, urllib2
# http://forum.fibaro.com/viewtopic.php?t=1741&postdays=0&postorder=asc&start=0
# use Device Spy from Developer Tools for UPnP to get UUID

HOST = "192.168.1.105"
PORT = 8080
UUID = "18d848f0-1dd2-11b2-bf00-000391e19ead"

VOD    = 361
POWER  = 116
N      = 174
EPG    = 365
PORTAL = 102

INFO   = 358
APP    = 367
OPT    = 357

VOL_P  = 115
VOL_M  = 114

UP     = 103
LEFT   = 105
OK     = 352
RIGHT  = 106
DOWN   = 108

PR_P   = 402
PR_M   = 403

BACK   = 158

STOP   = 128
REV    = 168 
PAUSE  = 119
PLAY   = 207
FF     = 159
REC    = 167


MUTE   = 113
PORTAL = 102
TEXT   = 388
LIST   = 395

RADIO  = 385

RED    = 398
GREEN  = 399
YELLOW = 400
BLUE   = 401

D1      =   2
D2      =   3
D3      =   4
D4      =   5
D5      =   6
D6      =   7
D7      =   8
D8      =   9
D9      =  10
D0      =  11

SETUP  =  367
STAR   =    1


keys={'VOD'    : 361,
      'POWER'  : 116,
      'N'      : 174,
      'EPG'    : 365,
      'HOME'   : 102,

      'INFO'   : 358,
      'APP'    : 367,
      'OPT'    : 357,

      'VOL_P'  : 115,
      'VOL_M'  : 114,

      'UP'     : 103,
      'LEFT'   : 105,
      'OK'     : 352,
      'RIGHT'  : 106,
      'DOWN'   : 108,

      'PR_P'   : 402,
      'PR_M'   : 403,

      'BACK'   : 158,

      'STOP'   : 128,
      'REV'    : 168,
      'PAUSE'  : 119,
      'PLAY'   : 207,
      'FF'     : 159,
      'REC'    : 167,


      'MUTE'   : 113,
      'PORTAL' : 102,
      'TEXT'   : 388,
      'LIST'   : 395,

      'RADIO'  : 385,

      'RED'    : 398,
      'GREEN'  : 399,
      'YELLOW' : 400, # music+ wimp
      'BLUE'   : 401, # netVOD+

      '1'      :   2,
      '2'      :   3,
      '3'      :   4,
      '4'      :   5,
      '5'      :   6,
      '6'      :   7,
      '7'      :   8,
      '8'      :   9,
      '9'      :  10,
      '0'      :  11,

      'SETUP'  : 367,
      'STAR'   :   1,
}

def send_soap(status, key):
    msg = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:ProcessInputEvent xmlns:u="urn:adbglobal.com:service:X_ADB_RemoteControl:1">
         <InputEvent>ev=%s,code=%d</InputEvent>
      </u:ProcessInputEvent>
   </s:Body>
</s:Envelope>""" % (status, key)
    url = "http://%s:%d/upnpfun/ctrl/uuid_%s/04" % (HOST, PORT, UUID)
    req = urllib2.Request(url, msg);
    req.add_header("SOAPACTION", '"urn:adbglobal.com:service:X_ADB_RemoteControl:1#ProcessInputEvent"');
    req.add_header('Content-type', 'application/xml');
    res = urllib2.urlopen(req).read();
    #print res

def send_key(key):
    #print key
    k =keys.get(key.upper(),-1)
    #print k
    send_soap("keydn", k)
    send_soap("keyup", k)
  
def main():
  send_key(sys.argv[1])
  
if __name__ == "__main__":
    main()
