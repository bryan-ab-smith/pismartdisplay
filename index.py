# Stdlib imports
import psutil
import datetime
from flask import Flask, render_template, jsonify
import configparser
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
import json

################## Configure block ##################

lights_enabled = ''
bridge_addr = ''
plugs_enabled = ''
news_feed = ''

configFile = 'static/config.json'

with open(configFile) as jsonFile:
    data = json.load(jsonFile)
    lights_enabled = data['lights_enabled']
    bridge_addr = data['bridge_address']
    plugs_enabled = data['plugs_enabled']
    news_feed = data['news_feed']

################## End of configure block ##################

# External imports
if lights_enabled == 'True':
    from phue import Bridge
if plugs_enabled == 'True':
    from pyHS100 import SmartPlug, Discover

app = Flask(__name__)

if lights_enabled == 'True':
    # https://github.com/studioimaginaire/phue
    # Set up the bridge object.
    bridge_obj = Bridge(bridge_addr)

    # Connect to the bridge
    bridge_obj.connect()

    # Get the api.
    bridge_obj.get_api()

plugList = {}

# Index route. Here, we send device information to the index template.
@app.route('/')
def index():

    lights = []

    if lights_enabled == 'True':
        # This gets the Philips Hue light info.
        # For each of the ligths available via the bridge, add it to the list of lights available.
        for light in bridge_obj.lights:
            # Append the light to the list.
            lights.append(light.name)

    if plugs_enabled == 'True':
        # https://github.com/GadgetReactor/pyHS100
        # This gets the TP-Link Kasa device info.
        # For each of the plugs available add it to the list of plugs.
        # Structure of plug list: [ 'name of light', 'ip address' ]
        for device in Discover.discover().keys():
            plugList[Discover.discover_single(device).alias] = device
            #plugs.append([Discover.discover_single(device).alias, device])

    # Get the boot time.
    # Source: https://github.com/SlapBot/stephanie-va/blob/master/Stephanie/Modules/system_module.py
    bootSeconds = psutil.boot_time()
    # Convert it to a datetime
    upSince = datetime.datetime.fromtimestamp(bootSeconds)

    # String format the datetime.
    bootTime = upSince.strftime('%a %b %d, %Y at %H:%M:%S')

    # Render the homepage.
    return render_template('index.html',
                           lightsEnabled=lights_enabled,
                           plugsEnabled=plugs_enabled,
                           lights=lights,
                           plugs=plugList,
                           bootTime=bootTime)


@app.route('/news')
def getNews():
    feedReq = urllib.request.urlopen(news_feed)
    feed = feedReq.read()
    doc = ET.fromstring(feed)

    arts = doc.findall('channel/item/title')
    descs = doc.findall('channel/item/description')

    news = [arts[0].text, descs[0].text, arts[1].text,
            descs[1].text, arts[2].text, descs[2].text]
    return jsonify(news)


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
    '''for device in Discover.discover().keys():
        plugs[Discover.discover_single(device).alias] = device'''
    if status == 'False':
        for devices in plugList.keys():
            plug = SmartPlug(plugList[devices])
            plug.turn_off()
    else:
        for devices in plugList.keys():
            plug = SmartPlug(plugList[devices])
            plug.turn_on()
    return 'Plugs toggled!'


@app.route('/plug/<status>/<name>')
def togglePlug(status, name):

    if status == 'False':
        plug = SmartPlug(plugList[name])
        plug.turn_off()
    else:
        plug = SmartPlug(plugList[name])
        plug.turn_on()
    return 'hi!'


@app.route('/reboot')
def rebootDevice():
    subprocess.Popen('sudo reboot', shell=True)


if __name__ == '__main__':
    app.debug = True

    # From: https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679.
    # I'm not really sure if this speeds things up but local JS and CSS files seem to really slow things down.
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port='9000', threaded=True)
