import sys, json, urllib2, datetime

URL = "http://192.168.1.7:8008/jsonrpc"
UUIDS = {
  "speakers"   : "7b25f7cb-26ca-4b1d-94ca-9efe4e517e60",
  "roller"     : "d0df5b02-5e46-4bd1-9b70-d9aa556691cc",
  "controller" : "d0b64506-edad-42f2-8c34-e690e6f24840",
  "thermostat" : "3aa331a5-2c75-4821-a617-014b4f46441c",
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
    if param in UUIDS.keys():
      print param
      uuid = UUIDS[param]
      msg["params"]["content"]["uuid"] = uuid
      msg["params"]["content"]["command"] = val      
      
      return agocontrol_send(msg)
    
    return ""

def agocontrol_set_level(device, level):
    #print param, val
    # 20 = 90%
    # 50 = 80%
    # 65 = 70%
    # 70 = 50%
    # 75 = 40%
    # 80 = 30%
    # 90 = 20%
    # 95 = 10%
    level = int(level)
    if level > 100:
      level = 100
    if level < 0:
      level = 0
    
    #print level
    if level < 15:
      val = 100
    if level >= 15:
      val = 95
    if level >= 25:
      val = 90
    if level >= 35:
      val = 80
    if level >= 45:
      val = 75
    if level >= 55:
      val = 70
    if level >= 75:
      val = 65
    if level >= 85:
      val = 50
    if level >= 95:
      val = 20
    if level >= 97:
      val = 0
    
    
    
    msg = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "message",
  "params": {
    "content": {
      "uuid": "",
      "command": "setlevel",
      "level": ""
    }
  }
}
    if device in UUIDS.keys():
      print device
      uuid = UUIDS[device]
      msg["params"]["content"]["uuid"]  = uuid
      msg["params"]["content"]["level"] = level      
      
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
  if len(sys.argv) < 4:
    print "wrong parameters count"
    print "usage: %s function[switch, setlevel] device command_value"
    exit(1)

  if sys.argv[1] == "switch":
    res = agocontrol_send_cmd(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == "setlevel":
    res = agocontrol_set_level(sys.argv[2], sys.argv[3])
  else:
    res = "unknown function %s" % sys.argv[1]
  print res
