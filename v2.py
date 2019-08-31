from flask import Flask, render_template
from phue import Bridge

from pyHS100 import SmartPlug, Discover

################## Configure block ##################

# This is the IP address of your Philips Hue bridge.
bridge_addr = '192.168.0.2'


################## End of configure block ##################

app = Flask(__name__)

# Set up the bridge object.
bridge_obj = Bridge(bridge_addr)

# Connect to the bridge
bridge_obj.connect()

# Get the api.
bridge_obj.get_api()

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


if __name__ == '__main__':
    app.debug = True

    # From: https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679.
    # I'm not really sure if this speeds things up but local JS and CSS files seem to really slow things down.
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port='9000', threaded=True)
