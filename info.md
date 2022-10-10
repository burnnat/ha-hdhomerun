## Overview
Custom component to view status of [HDHomeRun](https://www.silicondust.com/hdhomerun/) devices from Home Assistant. 

## Installation
This component requires the [libhdhomerun](https://github.com/Silicondust/libhdhomerun) library to function. Some distros may have a prebuilt package available, such as Ubuntu:

    apt install libhdhomerun4

Or Alpine Linux (i.e. Home Assistant docker):
    
    sudo docker exec -it homeassistant bash

    apk add libhdhomerun

Other systems may require building the library from source.

## Configuration:
```
auto-discovery on your network with ssdp.
or you can put an entry in configuration.yaml:
hdhomerun:
    # Host addresses are optional, if none are specified then entities will be populated by network discovery.
    sensor:
        - host: 192.168.1.10
        - host: 192.168.1.5
```
