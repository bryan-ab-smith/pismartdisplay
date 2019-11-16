## Stdlib imports
import configparser

## External imports
from flask import Flask, render_template
from phue import Bridge
from pyHS100 import SmartPlug, Discover

################## Configure block ##################

config = configparser.ConfigParser()
config.read('config')

lights_enabled = config['lights']['enabled']

# This is the IP address of your Philips Hue bridge.
bridge_addr = config['lights']['bridge_address']

plugs_enabled = config['plugs']['enabled']

################## End of configure block ##################

app = Flask(__name__)

# Set up the bridge object.
bridge_obj = Bridge(bridge_addr)

# Connect to the bridge
bridge_obj.connect()

# Get the api.
bridge_obj.get_api()

plugs = {}

# Index route. Here, we send device information to the index template.
@app.route('/')
def index():

    lights = []
    plugs = []

    # This gets the Philips Hue light info.
    # For each of the ligths available via the bridge, add it to the list of lights available.
    for light in bridge_obj.lights:
        # Append the light to the list.
        lights.append(light.name)

    # This gets the TP-Link Kasa device info.
    # For each of the plugs available add it to the list of plugs.
    # Structure of plug list: [ 'name of light', 'ip address' ]
    for device in Discover.discover().keys():
        plugs.append([Discover.discover_single(device).alias, device])

    # Render the homepage.
    return render_template('v2.html',
                           lightsEnabled=lights_enabled,
                           plugsEnabled=plugs_enabled,
                           lights=lights,
                           plugs=plugs)


@app.route('/light/<status>/<name>')
def toggleLight(status, name):
    if status == 'False':
        bridge_obj.set_light(name, 'on', False)
    else:
        bridge_obj.set_light(name, 'on', True)
    return 'hi!'


@app.route('/allLights/<status>')
def toggleAllLights(status):
    if status == 'False':
        for light in bridge_obj.lights:
            bridge_obj.set_light(light.name, 'on', False)
    else:
        for light in bridge_obj.lights:
            bridge_obj.set_light(light.name, 'on', True)
    return 'hi!'

@app.route('/allPlugs/<status>')
def toggleAllSwitches(status):
    for device in Discover.discover().keys():
        plugs[Discover.discover_single(device).alias] = device
    if status == 'False':
        for devices in plugs.keys():
            plug = SmartPlug(plugs[devices])
            plug.turn_off()
    else:
        for devices in plugs.keys():
            plug = SmartPlug(plugs[devices])
            plug.turn_on()
    return 'Plugs toggled!'

@app.route('/plug/<status>/<name>')
def togglePlug(status, name):
    if status == 'False':
        plug = SmartPlug(plugs[name])
        plug.turn_off()
    else:
        plug = SmartPlug(plugs[name])
        plug.turn_on()
    return 'hi!'

if __name__ == '__main__':
    app.debug = True

    # From: https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679.
    # I'm not really sure if this speeds things up but local JS and CSS files seem to really slow things down.
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port='9000', threaded=True)
