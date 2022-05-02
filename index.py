# Stdlib imports
import psutil
import datetime
from flask import Flask, render_template, jsonify
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
import json
import tinytuya
import time
import tuyactrl

with open('snapshot.json') as json_file:
   tuyasnap = json.load(json_file)


app = Flask(__name__)

# def turn_on(name):
# def turn_off(name):
# def bright_white(name):
# def evening(name):
# def white_setting(name,bright,temp):
# def office_bright():
# def office_evening():
# def office_off():
# def office_rainbow():


# Index route. Here, we send device information to the index template.
@app.route('/')
def index():

    lights = []

    # This gets the Philips Hue light info.
    # For each of the ligths available via the bridge, add it to the list of lights available.
    for light in tuyasnap["devices"]:
        # Append the light to the list.
        lights.append(light["name"])

    # Render the homepage.
    return render_template('index.html',
                           lightsEnabled="True",
                           lights=lights)


@app.route('/light/<name>/<status>')
def toggleLight(status, name):
    if status == 'True':
        tuyactrl.turn_on(name)
    else:
        tuyactrl.turn_off(name)

    return 'hi!'


@app.route('/allLights/<status>')
def toggleAllLights(status):
    match status:
        case 'off':
            tuyactrl.office_off()
            return 'lights out!'
        case 'bright':
            for light in tuyasnap["devices"]:
                tuyactrl.bright_white(light["name"])
                tuyactrl.turn_on(light["name"])
            return 'light bright!'
        case 'evening':
            for light in tuyasnap["devices"]:
                tuyactrl.evening(light["name"])
                tuyactrl.turn_on(light["name"])
            return 'little mood light!'
        case _:
            return 'Sorry Dave, afraid I can\'t do that'



@app.route('/reboot')
def rebootDevice():
    subprocess.Popen('sudo reboot', shell=True)


if __name__ == '__main__':
    app.debug = True

    # From: https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679.
    # I'm not really sure if this speeds things up but local JS and CSS files seem to really slow things down.
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port='80', threaded=True)

