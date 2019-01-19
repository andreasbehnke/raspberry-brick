# lego-berry
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

 * download raspbian lite: https://downloads.raspberrypi.org/raspbian_lite_latest
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
  for details on this configuration: https://weworkweplay.com/play/automatically-connect-a-raspberry-pi-to-a-wifi-network/
 * place empty SSH file in /boot/ssh to enable ssh after boot

 ## Configuration of raspberry pi using Ansible

 * TODO: Install ansible
 * first login with default pw to retrieve host key: ```ssh pi@raspberrypi.behnke.net``` password: raspberry
 *
