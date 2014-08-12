# -*- coding: utf-8 -*-
import flask

from shelljob import proc
import send_key2ncplus


app = flask.Flask(__name__)

@app.route('/_run_cmd')
def run_cmd():
    
    cmd = flask.request.args.get('fun', 0, type=str)
    param = flask.request.args.get('param', 0, type=str)

    g = proc.Group()
    #p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )
    path = "/home/pi/flask/%s"
    if cmd == 'on':
      script = path % "turn-tv-on.sh"
    elif cmd == 'off':
      script = path % "turn-tv-off.sh"
    elif cmd == 'source':
      script = path % ("switch-to-hdmiN.sh " + param)
    elif cmd == 'source2':
      script = path % "switch-to-hdmiN.sh 2"
    elif cmd == 'source3':
      script = path % "switch-to-hdmiN.sh 3"
    elif cmd == 'lamp_on':
      script = path % "../azw/turn_on.sh"
    elif cmd == 'lamp_off':
      script = path % "../azw/turn_off.sh"
    elif cmd == 'ncplus':
      res = send_key2ncplus.send_key(param)
      script = "echo '%s'" % res
    else:
      script = "echo 'Unknown command - check syntax'"
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


@app.route( '/stream/<cmd>' )
def stream(cmd):
    #print "<a href='stream/on'>turn on</a>"
    print "start"
    g = proc.Group()
    #p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )
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
        yield "List of available commands:<br/>"
        yield "<a href='/stream/on' >turn on</a><br/>"
        yield "<a href='/stream/off'>turn off</a><br/>"
        yield "<a href='/stream/source1'>HDMI source 1</a><br/>"
        yield "<a href='/stream/source2'>HDMI source 2</a><br/>"
        yield "<a href='/stream/source3'>HDMI source 3</a><br/>"
        yield "<a href='/stream/lamp_on'>Turn Socket on</a><br/>"
        yield "<a href='/stream/lamp_off'>Turn Socket off</a><br/>"
        yield "Current response:<p>"
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line
        yield "</p><br/>"

    return flask.Response( read_process() , mimetype= 'text/html' )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

