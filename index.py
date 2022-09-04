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
from matplotlib import colors
from joblib import Parallel, delayed


with open('snapshot.json') as json_file:
   tuyasnap = json.load(json_file)

app = Flask(__name__)

lights = []

# This gets the Philips Hue light info.
# For each of the ligths available via the bridge, add it to the list of lights available.
for light in tuyasnap["devices"]:
    # Append the light to the list.
    lights.append(light["name"])

lights.sort()

# Index route. Here, we send device information to the index template.
@app.route('/')
def index():
    # Render the homepage.
    return render_template('index.html',
                           lightsEnabled="True",
                           lights=lights)


@app.route('/light/<name>/<status>')
def toggleLight(status, name):
    match status:
        case 'off':
            tuyactrl.turn_off(name)
        case 'on':
            tuyactrl.turn_on(name)
        case 'bright':
            tuyactrl.bright_white(name)
            tuyactrl.turn_on(name)
        case 'evening':
            tuyactrl.evening(name)
            tuyactrl.turn_on(name)
        case _:
            return 'Sorry Dave, afraid I can\'t do that'
    return tuyactrl.status(name)


@app.route('/light/<name>/rgb/<r>/<g>/<b>')
def rgbLight(name,r,g,b):
    tuyactrl.color_setting(name,100,r,g,b)
    tuyactrl.turn_on(name)
    return tuyactrl.status(name)

@app.route('/light/all/rgb/<r>/<g>/<b>')
def rgbAllLight(r,g,b):
    outs = Parallel(n_jobs=-1)(delayed(rgbLight)(light,r,g,b) for light in lights)
    return str(outs)

@app.route('/light/<name>/color/<color>')
def colorLight(name,color):
    rgb = colors.to_rgb(color)
    r= int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    tuyactrl.color_setting(name,100,r,g,b)
    tuyactrl.turn_on(name)
    return tuyactrl.status(name)

@app.route('/light/all/color/<color>')
def colorAllLight(color):
    outs = Parallel(n_jobs=-1)(delayed(colorLight)(light,color) for light in lights)
    return str(outs)

@app.route('/light/<name>')
def getLightState(name):
    return tuyactrl.status(name)

@app.route('/light/all/<status>')
def toggleAllLights(status):
    match status:
        case 'off':
            Parallel(n_jobs=-1)(delayed(tuyactrl.turn_off)(light) for light in lights)
        case 'on':
            Parallel(n_jobs=-1)(delayed(tuyactrl.turn_on)(light) for light in lights)
        case 'bright':
            Parallel(n_jobs=-1)(delayed(tuyactrl.bright_white)(light) for light in lights)
            Parallel(n_jobs=-1)(delayed(tuyactrl.turn_on)(light) for light in lights)
        case 'evening':
            Parallel(n_jobs=-1)(delayed(tuyactrl.evening)(light) for light in lights)
            Parallel(n_jobs=-1)(delayed(tuyactrl.turn_on)(light) for light in lights)
        case _:
            return 'Sorry Dave, afraid I can\'t do that'
    return "Done"

@app.route('/reboot')
def rebootDevice():
    subprocess.Popen('sudo reboot', shell=True)


if __name__ == '__main__':
    app.debug = True

    # From: https://blog.socratic.org/the-one-weird-trick-that-cut-our-flask-page-load-time-by-70-87145335f679.
    # I'm not really sure if this speeds things up but local JS and CSS files seem to really slow things down.
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port='80', threaded=True)

