# Pi SmartScreen

A simple smart home and info display for the Raspberry Pi. Right now, you can control Philips Hue lights, TP-Link plugs and get time, weather (anywhere) and UV info (Australia only right now; UV observations courtesy of ARPANSA).

![](screenshot.png)


## Re-development (v2)

I designed this not to be something available for everyone and so the code isn't packaged in such a way as to make it "easy" for you. However, I am slowly working on making this more friendly to other setups, named _v2_ for now.

You can track progress in the various _v2_ files -- v2.py, v2.html, v2.js. These will eventually become the main Flask app. Don't expect this to work until it becomes the main script.

### Current status of v2
v2 runs and will control lights if properly configured (see the v2 Python script's configuration block at the top). Plugs don't work ~~and the internationalisation of the UV index doesn't work~~ (yet).

### Plan
| Idea                         | Notes                                                                                                                         | Status                                                                                                                               |
| ---------------------------- |:-----------------------------------------------------------------------------------------------------------------------------:| ------------------------------------------------------------------------------------------------------------------------------------:|
| Dyanmic device creation      | Right now, the app is hard coded for a specific smart device configuration. This should be generated automatically.           | Initial work on this has been done (eg. light controls are now dynamically generated based on the lights connected to your bridge).  |
| Configuration options        | Having a config file to control user-specific needs.                                                                          | Initial work is done.                                                                                                                |
| Plug support                 | Re-adding TP-Link Kasa plus support.                                                                                          | Hasn't started yet.                                                                                                                  |


### Current Version

## Requirements
- Python 3
- Flask, phue (Philips Hue) and pyHS100 (TP-Link Kasa Plugs) modules. Right now, the setup supports Philips Hue lights and TP-Link Kasa plugs:
    
        pip3 install flask phue pyhs100

## Setup

### RPi and Browser
1. Install minimal Raspbian instance on your RPi. I used a RPi 3 here but I suppose any RPi could work.
2. Install Openbox and start Chromium in kiosk mode. I followed [these instructions](https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/) to do all of this.

### Application
1. Once the device is setup up, if you restart your Pi, the application will (naturally) not load. Everything to get the app displayed is up except for the app itself. At this point, you'll want to SSH into your Pi.
2. Clone the code and tweak as necessary. This app is hard coded for my device configuration so you're going to have to edit quite a bit (some easier config is coming). You will want to edit the devices and you will need to add in weather and UV index info. The JS expects an OpenWeather URL (see line 35 of static/js/main.js) and an ARPANSA UV index city name (see line 52 of static/js/main.js). See code for details about getting those. The latter of these two -- the UV index -- is Australian specific so if you aren't here down under, you'll need to replace that UV get request entirely or take out that functionality (to do so, take out lines 45-57 of static/js/main.js and and line 32 of templates/index.html).
3. Install the required Python modules: `pip3 install flask phue pyHS100`
4. Move static/config.json.template to static/config.json and edit the variable as needed (see Config section below).
5. Copy the smartscreen.service to */etc/systemd/system*. Once there, tweak it as necessary (likely line 8 only, the *WorkingDirectory*, which is where the index.py file is).
6. Run the following: `sudo systemctl enable smartscreen && sudo reboot`. This will enable the smartscreen service and reboot the device. Assuming everything goes well, you should be greeted with your smartscreen display.

With this setup, your screen will stay on forever. You'll want to install a screensaver if you're using something like the official LCD screen (as I am).

### Config

#### static/config.json
This configuration file allows you to set up some custom settings to set the screen up for your needs. More configuration coming but what's below works as of now. All of these only work for v2 as of now.

| Key            | Value                      | Description/Note                                                                                                                     |
| -------------- |:--------------------------:| ------------------------------------------------------------------------------------------------------------------------------------:|
| owAPI_key      | API Key (string)           | This gives you access to OpenWeather data. See [here](https://openweathermap.org/appid) for information about getting the key.       |
| ow_loc         | Location for weather data  | This should be in the format `city,country_code`. For example, `Toronto,CA`                                                          |
| ow_units       | Units for the weather data | This should be either `metric` or `imperial`                                                                                         |
| ouvAPI_key     | API Key (string)           | This gives you access to OpenUV data. See [here](https://www.openuv.io/) for more information about getting the key.                 |

NOTE: I'm not convinced that OpenWeather and OpenUV are super accurate (eg. ARPANSA data values in Australia are not the same as OpenUV data and the former is a more authoritative source). So, the data providers may change. In the meantime, this opens up the app to all people and provides, at the least, an approximate set of weather and UV data points.

#### /config
| Key            | Value                      | Description/Note                                                                                                                     |
| -------------- |:--------------------------:| ------------------------------------------------------------------------------------------------------------------------------------:|
| lights -> enabled     | `True` or `False`           | Enable or disable the light control functionality.      |
| lights -> bridge_address     | IP Address of the Philips Hue Bridge           | The IP address of the Philips Hue bridge. If you don't know what this is, open up the Philips Hue app -> Settings -> Hue Bridges -> Info icon -> IP Address.      |
| plugs -> enabled     | `True` or `False`           | Enable or disable the plug control functionality.      |

### Testing

WHile this is designed to work on a Raspberry Pi with a small touchscreen, it's just a web app at heart so it will run anywhere Python is supported (ie. basically anywhere). So, you can run it on your local computer:

    python3 index.py

Once that's running, navigate to _http://localhost:9000_.

### Things to note
1. This is developed with the official RPi LCD screen used as the reference display. This means that the UI is designed to fit nicely into a 800x480 space. This is not to say that it won't work elsewhere but that small tweaks may be required of you if you use a very different resolution.