# HA-HDHomeRun

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

A custom component to view status of [HDHomeRun](https://www.silicondust.com/hdhomerun/) devices from Home Assistant.

## Installation

This component requires the [libhdhomerun](https://github.com/Silicondust/libhdhomerun) library to function.  

### Manual Dependency Installation

Some distros have a prebuilt package available, such as Ubuntu:

```bash
apt install libhdhomerun4
```

Or Alpine Linux (i.e. Home Assistant docker):

```bash
apk add libhdhomerun
```

Other systems may require building the library from source.

## Configuration

```yml
hdhomerun:
    # Host addresses are optional, if none are specified then entities will be populated by network discovery.
    sensor:
        - host: 192.168.1.10
        - host: 192.168.1.5
```
