import sys, json, urllib2, datetime

URL = "http://192.168.1.110:8008/jsonrpc"
UUIDS = {
  "speakers" : "af088742-c0a3-473f-a5e8-7bd59d735585",
  "controller" : "c4a10ff0-6d7e-4630-ae4b-c0cd6e0af117",
  }

def agocontrol_send(msg, timeout=1):
    #print msg
    req = urllib2.Request(URL)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Cache-Control', 'no-cache')
    
    response = ""
    try:
      response = urllib2.urlopen(req, json.dumps(msg), timeout=timeout).read()
    except:
      pass
    
    return response


def agocontrol_send_cmd(param, val):
    #print param, val
    msg = {
        "jsonrpc": "2.0",
        "method": "message",
        "params": {
          "content": {
            "command": "",
            "uuid": ""
          }
        },
        "id": 1
      }
    if param == "speakers":
      uuid = UUIDS[param]
      msg["params"]["content"]["uuid"] = uuid
      msg["params"]["content"]["command"] = val      
      
      return agocontrol_send(msg)
    
    return ""

def agocontrol_subscribe():

    msg = {
          "method": "subscribe",
          "id": 1,
          "jsonrpc": "2.0"
        }
    print "subscribe"
    return agocontrol_send(msg)

def agocontrol_getevent(uuid=None):
    
    if uuid == None:
      res = agocontrol_subscribe()
      uuid = json.loads(res)["result"]

    msg = {
      "method": "getevent",
      "params": {
          "uuid": uuid
      },
      "id": 2,
      "jsonrpc": "2.0"
    }

    res = agocontrol_send(msg, 10000)
    res = json.loads(res)["result"]
    res = json.dumps(res, indent=4, separators=(',', ': ') )
    print datetime.datetime.now().replace(microsecond=0).time().isoformat(), res
    
    return (res, uuid)

def main():
  uuid=None
  while True:
    res, uuid = agocontrol_getevent(uuid)

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "wrong parameters count"
    exit(1)

    #res = agocontrol_send_cmd(sys.argv[1], sys.argv[2])
    #print res
