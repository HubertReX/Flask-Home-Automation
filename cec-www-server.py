# -*- coding: utf-8 -*-
import flask
from flask.ext.assets import Environment, Bundle

from shelljob import proc
import send_key2ncplus
import send_x10_to_htpc
import wol

app = flask.Flask(__name__, static_folder='static', static_url_path='')

@app.route('/_run_cmd')
def run_cmd():
    # example call: http://pi:5000/_run_cmd?fun=ncplus&param=info
    # example call: http://pi:5000/_run_cmd?fun=ZWAVE&param=speakers&val=on
    
    cmd   = flask.request.args.get('fun',   0, type=str)
    param = flask.request.args.get('param', 0, type=str)
    val   = flask.request.args.get('val',   0, type=str)

    g = proc.Group()

    path = "/home/pi/flask/%s"
    if cmd == 'TV':
      script = path % ("cmd-processor-TV.sh " + param)
    elif cmd == 'ZWAVE':
      script = path % ("cmd-processor-Z-Wave.sh " + param + " " + val)
    elif cmd == 'NCPLUS':
      script = "" # path % ("cmd-processor-NCPLUS.sh " + param)
      rresultses = send_key2ncplus.send_key(param)
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

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/ncplus')
def ncplus():
    return flask.render_template('ncplus.html')

@app.route('/htpc')
def x10():
    return flask.render_template('htpc.html')

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

