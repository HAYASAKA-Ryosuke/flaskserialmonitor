import time
from flask import Flask, Response, request, render_template
import random
import serial
from serial.tools import list_ports

class SerialMonitor(object):
    def __init__(self,COM,baudrate):
        self.ser=serial.Serial(COM,baudrate)
    def read(self):
        self.ser.readline()
    def close(self):
        self.ser.close()
serial=SerialMonitor('/dev/usb',115200)

app = Flask(__name__)

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while(True):
                random1=str(random.random()*10)
                random2=str(random.random()*10)
                yield "data: %s,%s,%s \n\n" % (serial.read(),random1,random2)
                time.sleep(.1)
        return Response(events(),content_type='text/event-stream')
    return render_template('index.html')
app.run()


