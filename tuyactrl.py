import tinytuya
import json
import time

#tinytuya.set_debug(True)

with open('snapshot.json') as json_file:
     data = json.load(json_file)

# Turn on a device by name
def turn_on(name):
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nTurning On: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    d.turn_on()

# Turn off a device by name
def turn_off(name):
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nTurning Off: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    d.turn_off()

def bright_white(name):
    white_setting(name,100,100)

def evening(name):
    white_setting(name,90,0)


def white_setting(name,bright,temp):
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nSetting White: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    d.set_brightness_percentage(brightness=bright)
    d.set_colourtemp_percentage(colourtemp=temp)

def color_setting(name,bright,r,g,b):
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nSetting White: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    d.set_brightness_percentage(brightness=bright)
    d.set_colour(int(r),int(g),int(b))

def office_bright():
    for light in data["devices"]:
        bright_white(light["name"])
        turn_on(light["name"])

def office_evening():
    for light in data["devices"]:
        evening(light["name"])
        turn_on(light["name"])

def office_off():
    for light in data["devices"]:
        turn_off(light["name"])

def office_rainbow():
    rainbow = {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0],
               "green": [0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95],
               "violet": [139, 0, 255]}

    # Flip through colors of rainbow - set_colour(r, g, b):
    for light in data["devices"]:
        for x in range(10):
            for i in rainbow:
                r = rainbow[i][0]
                g = rainbow[i][1]
                b = rainbow[i][2]

                d = tinytuya.BulbDevice(light["id"], light["ip"], light["key"])
                d.set_version(float(light["ver"]))
                d.set_colour(r, g, b)
                d.turn_on()
                time.sleep(2)

def status(name):
    hr_status = {}
    # find the right item that matches name
    for item in data["devices"]:
        if item["name"] == name:
            break
    print("\nStatus For: %s" % item["name"])
    d = tinytuya.BulbDevice(item["id"], item["ip"], item["key"])
    d.set_version(float(item["ver"]))
    status = d.status()
    hr_status["light_on"] = status["dps"]["20"]
    hr_status["mode"] = status["dps"]["21"]
    hr_status["bright"] = status["dps"]["22"]
    hr_status["temp"] = status["dps"]["23"]
    hr_status["color_hex"] = status["dps"]["24"]
    return hr_status
    
    
