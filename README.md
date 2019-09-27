# ha-hdhomerun
Custom component to enable HDHomeRun integration for Home Assistant.

## Configuration
    hdhomerun:
        # Host addresses are optional, if none are specified then entities will be populated by network discovery.
        sensor:
            - host: 192.168.1.10
            - host: 192.168.1.5