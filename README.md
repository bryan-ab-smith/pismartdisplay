# Pi SmartScreen

Flask app for the smart screen and device hub.

This was really only meant for my own setup at home so the code isn't very "flexible." However, it might be of use so play with it as you'd like.

## Requirements
- Python 3
- phue (Philips Hue) and pyHS100 (TP-Link Kasa Plugs) modules. Again, as this was written for my own setup, this is very "me specific."

## Setup

### RPi and Browser
1. Install minimal Raspbian instance on your RPi. I used a RPi 3 here but I suppose any RPi could work.
2. Install Openbox and start Chromium in kiosk mode. I followed [these instructions](https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode/) to do all of this.

### Application
1. Once the device is setup up, if you restart your Pi, the application will (naturally) not load. Everything to get the app displayed is up except for the app itself. At this point, you'll want to SSH into your Pi.
2. Clone the code and tweak as necessary. This app is hard coded for my device configuration so you're going to have to edit quite a bit. You will want to edit the devices and you will need to add in weather and UV index info. The JS expects an OpenWeather URL (see line 35 of static/js/main.js) and an ARPANSA UV index city name (see line 52 of static/js/main.js). See code for details about getting those. The latter of these two -- the UV index -- is Australian specific so if you aren't here down under, you'll need to replace that UV get request entirely or take out that functionality (to do so, take out lines 45-57 of static/js/main.js and and line 32 of templates/index.html).
3. Install the required Python modules: `pip3 install phue pyHS100`
4. Copy the smartscreen.service to */etc/systemd/system*. Once there, tweak it as necessary (likely line 8 only, the *WorkingDirectory*, which is where the index.py file is).
5. Run the following: `sudo systemctl enable smartscreen && sudo reboot`. This will enable the smartscreen service and reboot the device. Assuming everything goes well, you should be greeted with your smartscreen display.

With this setup, your screen will stay on forever. You'll want to install a screensaver if you're using something like the official LCD screen (as I am).