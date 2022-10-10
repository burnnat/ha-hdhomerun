# ha-hdhomerun
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Custom component to enable [HDHomeRun](https://www.silicondust.com/hdhomerun/) integration for Home Assistant.

This version has more features: [https://github.com/uvjim/hass_hdhomerun] (https://github.com/uvjim/hass_hdhomerun)

Creates an entity for each tuner found and attributes for signal_strength, SNR and CPS for the currently tuned to channel.
Useful for monitoring your antenna system; signal_strength and SNR should be good indicators that antenna, cabling, preamp and splitters are all in order.

See overview and configuration information [here](info.md).

To graph signal_strength, SNR and CPS over time, create templates, this is what I have in configuration.yaml:

    sensor:
      - platform: template
        sensors:
          hdhomerun_tuner_10686756_0_signal_strength:
            value_template: "{{state_attr('sensor.hdhomerun_tuner_10686756_0','signal_strength')}}"
           unit_of_measurement: '%'
          hdhomerun_tuner_10686756_0_snr:
            value_template: "{{state_attr('sensor.hdhomerun_tuner_10686756_0','snr')}}"
            unit_of_measurement: '%'
          hdhomerun_tuner_10686756_0_bps:
            value_template: "{{state_attr('sensor.hdhomerun_tuner_10686756_0','bps')}}"
            unit_of_measurement: 'bps'
          hdhomerun_tuner_10686756_1_signal_strength:
            value_template: "{{state_attr('sensor.hdhomerun_tuner_10686756_1','signal_strength')}}"
            unit_of_measurement: '%'
          hdhomerun_tuner_10686756_1_snr:
            value_template: "{{state_attr('sensor.hdhomerun_tuner_10686756_1','snr')}}"
            unit_of_measurement: '%'
          hdhomerun_tuner_10686756_1_bps:
            value_template: "{{state_attr('sensor.hdhomerun_tuner_10686756_1','bps')}}"
            unit_of_measurement: 'bps'

