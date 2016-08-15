from subprocess import call
import atexit
import os

class App(object):
    def __init__(self, lang='en', filename='log.fifo', time=100):
        self.lang     = lang
        self.filename = filename
        self.time     = 100

        if not os.path.exists(filename):
            os.mkfifo(self.filename)

        call(['logkeys', '--start', '--output=%s' % filename, 
        '--no-timestamps', '--no-func-keys'])

        self.fd = open(self.filename, 'r')
        atexit.register(lambda: call(['logkeys',  '--kill']))

    def run(self):
        while True:
            data = self.fd.readline()
            call(['espeak', '-v', self.lang, '"%s"' % data, 
            '-s %s' % self.time,])

