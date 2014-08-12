import urllib2, base64, sys

USERNAME = 'player'
PASSWORD = 'konrad1'
BASE_URL = "http://192.168.1.100:8008/?%s"

BUTTONS = {
'power': 'Power',
'live_tv': 'ChannelSearch',
'rec_tv': 'Snapshot',
'photo': 'Photo',
'music': 'Music',
'dvd_menu': 'DVD',
'video': 'VCR',

'guide': 'MTTrack', # VideoDesktop
'text': 'TXT', 

'red': 'Red',
'yellow': 'Yellow',
'blue': 'Blue',
'green': 'Green',

'left': 'Left',
'right': 'Right',
'up': 'Up',
'down': 'Down',
'ok': 'Ok',

'vol_u': 'VolumeUp',
'vol_d': 'VolumeDown',
'mute': 'Mute',

'pr_p': 'ChannelUp',
'pr_m': 'ChannelDown',

'0': 'Num0',
'1': 'Num1',
'2': 'Num2',
'3': 'Num3',
'4': 'Num4',
'5': 'Num5',
'6': 'Num6',
'7': 'Num7',
'8': 'Num8',
'9': 'Num9',

'star': 'AcquireImage',
'hash': 'EditImage',

'back': 'Delete',
'info': 'TVPreview',


'special': 'Setup',
'setup': 'Setup',

'play': 'Play',
'stop': 'Stop',
'pause': 'Pause',
'rewind': 'Rewind',
'ff': 'Forward',
'next': 'NextTrack',
'prev': 'PreviousTrack',
'rec': 'Record',
}

def send_x10_cmd(key):
  if key not in BUTTONS.keys():
    return "wrong key"
  cmd = BASE_URL % BUTTONS[key]

  request = urllib2.Request(cmd)
  request.add_header('Authorization', b'Basic ' + base64.b64encode(USERNAME + b':' + PASSWORD))
  try:
    urllib2.urlopen(request, timeout=1).read()

    result = "ok"
  except:
    result = "error"
  return result

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print "missing key paramter"
    exit(1)

  res = send_x10_cmd(sys.argv[1])
  print res

