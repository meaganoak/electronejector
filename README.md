# electronejector
code to run the electron ejector science demo

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev
sudo apt-get install -y portaudio19-dev python3-pyaudio
sudo pip install pyaudio --break-system-packages
sudo pip install rpi_ws281x pygame gif_pygame board adafruit-blinka adafruit-circuitpython-neopixel --break-system-packages
sudo pip uninstall neopixel
