__author__ = 'hnafalsk'
import os

PIPE_NAME = 'jasper_pipe_mic'
if not os.path.exists(PIPE_NAME):
    os.mkfifo(PIPE_NAME)

pipein = open(PIPE_NAME, 'r', "utf-8")
while True:
        line = pipein.readline()[:-1]
        if line:
            print '%d: %s' % (len(line), line)
