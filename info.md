# HA-HDHomeRun

A custom component to view status of [HDHomeRun](https://www.silicondust.com/hdhomerun/) devices from Home Assistant.

## Installation

This component requires the [libhdhomerun](https://github.com/Silicondust/libhdhomerun) library to function.  
See [ReadMe](https://github.com/Berserkir-Wolf/ha-hdhomerun/blob/master/README.md) for full instructions.  

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
