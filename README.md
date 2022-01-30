# raspberry-brick
Use raspberry pi for controlling lego power function models using any programming language you like.

## Hardware

 * raspberry pi 3
 * raspberry pi camera (optional but a very good extensions for autonomous robotics)
 * motor controller:
    * https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi
    * https://www.adafruit.com/product/2348      
 * lego power function extension cable: https://shop.lego.com/de-DE/LEGO-Power-Functions-Verl%C3%A4ngerungskabel-8886
 * 5V UBEC for powering raspberry from lego battery pack: https://www.adafruit.com/product/1385

## Pre Configuration

 * download latest raspios lite image from https://www.raspberrypi.com/software/operating-systems/
 * write image to SD card
 * place WIFI pre configuration file before first boot /boot/wpa_supplicant.conf:
   (you can find pre configuration file examples in folder pre-setup)

  ```
  country=US
  update_config=1
  ctrl_interface=/var/run/wpa_supplicant

  network={
    ssid="your ssid"
    psk="your pre shared key"
  }
  ```
  for details on this configuration: https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi
 * place empty SSH file in /boot/ssh to enable ssh after boot

 ## Configuration of raspberry pi using Ansible

 * TODO: Install ansible
 * first login with default pw to retrieve host key: ```ssh pi@raspberrypi.behnke.net``` password: raspberry
 *
