# -*- coding: utf-8 -*-
import flask
from flask.ext.assets import Environment, Bundle

from shelljob import proc
import os
import send_key2ncplus
import send_x10_to_htpc
import wol
import zwave

PIPE_NAME = '/home/pi/flask/jasper_pipe_mic'
if not os.path.exists(PIPE_NAME):
    os.mkfifo(PIPE_NAME)


class PolishRequest(flask.Request):
     url_charset = 'utf-8'

app = flask.Flask(__name__, static_folder='static', static_url_path='')
app.request_class = PolishRequest
app.url_map.charset = 'utf-8'

@app.route('/_run_cmd')
def run_cmd():
    # example call: http://pi:5000/_run_cmd?fun=ncplus&param=info
    # example call: http://pi:5000/_run_cmd?fun=ZWAVE&param=speakers&val=on
    
    cmd   = flask.request.args.get('fun',   "", type=str)
    param = flask.request.args.get('param', "", type=str)
    val   = flask.request.args.get('val',   "", type=str)

    g = proc.Group()

    path = "/home/pi/flask/%s"
    if cmd == 'TV':
      script = path % ("cmd-processor-TV.sh " + param)
    elif cmd == 'ZWAVE':
      script = "" # path % ("cmd-processor-Z-Wave.sh " + param + " " + val)
      results = zwave.agocontrol_send_cmd(param, val)
    elif cmd == 'NCPLUS':
      script = "" # path % ("cmd-processor-NCPLUS.sh " + param)
      results = send_key2ncplus.send_key(param)
    elif cmd == 'X10':
      script = "" #path % ("cmd-processor-X10.sh " + param)
      results = send_x10_to_htpc.send_x10_cmd(param)
    elif cmd == 'WOL':
      script = "" # path % ("cmd-processor-WOL.sh " + param)
      results = wol.main(param)
    else:
      script = "echo 'Unknown command - check syntax: %s %s'" % (cmd, param)
    
    if script != "":
      p = g.run(["bash", "-c", script])

      response = ""
      def read_process():
          response = ""
          while g.is_pending():
              lines = g.readlines()
              for proc, line in lines:
                  response = response + line
          return response

      results = read_process()
    return flask.jsonify(result=results.replace("\n",""))

@app.route('/_voice_cmd')
def voice_cmd():
    #for arg in flask.request.args:
    #    print repr(flask.request.args[arg])
    #flask.request.args.get('cmd',  "error", type=str)

    #print "got cmd %s" % repr(cmd)
    results = "ok"
    try:
        cmd = flask.request.args['cmd']
        print cmd
        #if isinstance(cmd, unicode):
        #    cmd = cmd.decode('utf-8')
        print cmd
        pipeout = os.open(PIPE_NAME, os.O_WRONLY|os.O_NONBLOCK)
        print "opened"
        os.write(pipeout, "%s\n" % cmd)
        print "write"
        os.close(pipeout)
    except Exception, e:
        print "error using named pipe: %s" % repr(e)
        results = "error"
    return flask.jsonify(result=results.replace("\n",""))

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/ncplus')
def ncplus():
    return flask.render_template('ncplus.html')

@app.route('/zwave')
def myzwave():
    return flask.render_template('zwave.html')

@app.route('/htpc')
def x10():
    return flask.render_template('htpc.html')

@app.route('/speech')
def speech():
    return flask.render_template('webspeechdemo.html')

@app.route('/voice')
def voice():
    return flask.render_template('voice_commands.html')

@app.route( '/stream/<cmd>' )
def stream(cmd):
    #depricated - use index.html instead!
    g = proc.Group()

    path = "/home/pi/flask/%s"
    if cmd == 'on':
      script = path % "turn-tv-on.sh"
    elif cmd == 'off':
      script = path % "turn-tv-off.sh"
    elif cmd == 'source1':
      script = path % "switch-to-hdmiN.sh 1"
    elif cmd == 'source2':
      script = path % "switch-to-hdmiN.sh 2"
    elif cmd == 'source3':
      script = path % "switch-to-hdmiN.sh 3"
    elif cmd == 'lamp_on':
      script = path % "../azw/turn_on.sh"
    elif cmd == 'lamp_off':
      script = path % "../azw/turn_off.sh"
    else:
      script = "echo 'Unknown command - check syntax'"
    p = g.run(["bash", "-c", script])

    def read_process():
        yield "Current response:<p>"
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line
        yield "</p><br/>"

    return flask.Response( read_process() , mimetype= 'text/html' )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

