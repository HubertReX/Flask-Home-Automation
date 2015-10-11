# -*- coding: utf-8 -*-
import socket
import base64
from time import sleep
from types import ClassType

TV_ACTIONS = (
('Up',       'Navigational Control Up',    'KEY_UP'),
('Down',     'Navigational Control Down',  'KEY_DOWN'),
('Left',     'Navigational Control Left',  'KEY_LEFT'),
('Right',    'Navigational Control Right', 'KEY_RIGHT'),
('Enter',    'Navigational Control Enter', 'KEY_ENTER'),
('Menu',     'Show settings menu',         'KEY_MENU'),
('VolUp',    'Volume up',                  'KEY_VOLUP'),
('VolDown',  'Volume down',                'KEY_VOLDOWN'),
('Return',   'Return (menu navigation)',   'KEY_RETURN'),
('Source',   'Switch to next HDMI source', 'KEY_HDMI'),
('ChUp',     'Channel up',                 'KEY_CHUP'),
('ChDown',   'Channel down',               'KEY_CHDOWN'),
('Info',     'Display info',               'KEY_INFO'),
('Mute',     'Toggle mute' ,               'KEY_MUTE'),
('PMode',    'Picture mode' ,              'KEY_PMODE'),
('Power',    'Toggle power' ,              'KEY_POWER'),
('PwrOn',    'Power on' ,                  'KEY_POWERON'),
('PwrOff',   'Power off' ,                 'KEY_POWEROFF'),
('Rec',      'Start recording' ,           'KEY_REC'),
('StbMode',  'Stand by mode (?)' ,         'KEY_STB_MODE'),
('Social',   'Social app (?)' ,            'KEY_TURBO'),
('Man',      'E-Manual (?)' ,              'KEY_TOPMENU'),
('3D',       'Switching between 3D modes', 'KEY_PANNEL_CHDOWN'),
)

class smartTV():

    def __init__(self):
      self.TV_IP   = "192.168.1.2"
      self.TV_PORT = 55000
      self.PC_IP   = "192.168.1.7"
      self.PC_MAC  = "f4-6d-04-93-11-82"

      #What the iPhone app reports
      self.appString = "iphone..iapp.samsung"
      #Might need changing to match your TV type
      self.tvAppString = "iphone.PS51E550.iapp.samsung"
      #What gets reported when it asks for permission
      self.remoteName = "Python Samsung Remote" 
      self.sock = None

    # Function to send keys
    def sendKey(self, skey):
        if not self.sock:
            self.connect()
        messagePart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(skey))) + chr(0x00) + base64.b64encode(skey)
        part3 = chr(0x00) + chr(len(self.tvAppString)) + chr(0x00) + self.tvAppString + chr(len(messagePart3)) + chr(0x00) + messagePart3
        try:
          self.sock.send(part3)
        except:
          self.connect()
          self.sock.send(part3)
          

    def connect(self):
        # Open Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        #try:
        self.sock.connect((self.TV_IP, self.TV_PORT))
        
        #except:
        #  print('Connection with %s was not sucessfull!' % self.TV_IP)
        #  exit(1)

        # First configure the connection
        ipEncoded  = base64.b64encode(self.PC_IP)
        macEncoded = base64.b64encode(self.PC_MAC)
        messagePart1 = chr(0x64) + chr(0x00) + chr(len(ipEncoded)) \
            + chr(0x00) + ipEncoded + chr(len(macEncoded)) + chr(0x00) \
            + macEncoded + chr(len(base64.b64encode(self.remoteName))) + chr(0x00) \
            + base64.b64encode(self.remoteName)

        part1 = chr(0x00) + chr(len(self.appString)) + chr(0x00) + self.appString \
            + chr(len(messagePart1)) + chr(0x00) + messagePart1
        self.sock.send(part1)

        messagePart2 = chr(0xc8) + chr(0x00)
        part2 = chr(0x00) + chr(len(self.appString)) + chr(0x00) + self.appString \
            + chr(len(messagePart2)) + chr(0x00) + messagePart2
        self.sock.send(part2)
    
    def disconnect(self):
        # Close the socket when done
        if self.sock:
            self.sock.close()
            self.sock = None



def main():
  sTV = smartTV()
  sTV.sendKey('KEY_VOLUP')
  sTV.disconnect()
  #print res
  
if __name__ == "__main__":
    main()
