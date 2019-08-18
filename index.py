from flask import Flask, render_template
from phue import Bridge

from pyHS100 import SmartPlug, Discover

app = Flask(__name__)

plugs = {}

@app.route('/')
def index():
    for device in Discover.discover().keys():
        plugs[Discover.discover_single(device).alias] = device
    return render_template('index.html')

@app.route('/bedroomLightOn')
def bedroomLightOn():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    bridge.set_light('Bedroom', 'on', True)
    return 'Hi!'

@app.route('/bedroomLightOff')
def bedroomLightOff():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    bridge.set_light('Bedroom', 'on', False)
    return 'Hi!'

@app.route('/deskLampLightOn')
def deskLampOn():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    bridge.set_light('Living Room Lamp', 'on', True)
    return 'Hi!'

@app.route('/deskLampLightOff')
def deskLampOff():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    bridge.set_light('Living Room Lamp', 'on', False)
    return 'Hi!'

@app.route('/frontHallLightOn')
def frontHallLampOn():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    bridge.set_light('Front Hall', 'on', True)
    return 'Hi!'

@app.route('/frontHallLightOff')
def frontHallLampOff():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    bridge.set_light('Front Hall', 'on', False)
    return 'Hi!'

@app.route('/allLightsOn')
def allLightsOn():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    for light in bridge.lights:
        bridge.set_light(light.name, 'on', True)
    return 'Hi!'

@app.route('/allLightsOff')
def allLightsOff():
    bridge = Bridge('192.168.0.2')
    bridge.connect()
    bridge.get_api()

    for light in bridge.lights:
        bridge.set_light(light.name, 'on', False)
    return 'Hi!'

@app.route('/fanSwitchOn')
def fanSwitchOn():
    plug = SmartPlug(plugs['Fan'])
    plug.turn_on()
    return 'Hi!'

@app.route('/fanSwitchOff')
def fanSwitchOff():
    plug = SmartPlug(plugs['Fan'])
    plug.turn_off()
    return 'Hi!'

@app.route('/dehumidSwitchOn')
def dehumidSwitchOn():
    plug = SmartPlug(plugs['Dehumidifier'])
    plug.turn_on()
    return 'Hi!'

@app.route('/dehumidSwitchOff')
def dehumidSwitchOff():
    plug = SmartPlug(plugs['Dehumidifier'])
    plug.turn_off()
    return 'Hi!'

@app.route('/allSwitchesOn')
def allSwitchesOn():
    dehumid = SmartPlug(plugs['Fan'])
    dehumid.turn_on()

    fan = SmartPlug(plugs['Dehumidifier'])
    fan.turn_on()
    return 'Hi!'

@app.route('/allSwitchesOff')
def allSwitchesOff():
    dehumid = SmartPlug(plugs['Fan'])
    dehumid.turn_off()

    fan = SmartPlug(plugs['Dehumidifier'])
    fan.turn_off()
    return 'Hi!'

if __name__ == '__main__':
    app.debug = True

    # From: https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679.
    # I'm not really sure if this speeds things up but local JS and CSS files seem to really slow things down.
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port='9000', threaded=True)