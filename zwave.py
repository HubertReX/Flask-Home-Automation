import sys, json, urllib2

URL = "http://192.168.1.110:8008/jsonrpc"
UUIDS = {
  "speakers" : "af088742-c0a3-473f-a5e8-7bd59d735585",
  "controller" : "c4a10ff0-6d7e-4630-ae4b-c0cd6e0af117",
  }

def agocontrol_send_cmd(param, val):
    
    msg_on = {
        "jsonrpc": "2.0",
        "method": "message",
        "params": {
          "content": {
            "command": "on",
            "uuid": ""
          }
        },
        "id": 1
      }
    msg_off = {
        "jsonrpc": "2.0",
        "method": "message",
        "params": {
          "content": {
            "command": "off",
            "uuid": ""
          }
        },
        "id": 1
      }

    req = urllib2.Request(URL)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Cache-Control', 'no-cache')
    
    data = {}
    response = None
    if param == "speakers":
      uuid = UUIDS[param]
      if val == "on":
        msg = msg_on
      else:
        msg = msg_off
      
      msg["params"]["content"]["uuid"] = uuid
      
      try:
        response = urllib2.urlopen(req, json.dumps(msg), timeout=1).read()
      except:
        pass
    
    return response


if __name__ == "__init__":
  if len(sys.argv) < 3:
    print "wrong parameters count"
    exit(1)

    res = agocontrol_send_cmd(sys.argv[1], sys.argv[2])
    print res
