# Sequent Microsystems Multi-IO Home Assistant Integration

Integrate [Multi-IO](https://sequentmicrosystems.com/products/multi-io-8-layer-stackable-hat-for-raspberry-pi)
seamlessly with Home Assistant, bringing all your custom functionality into the Home Assistant ecosystem for enhanced control, automation, and ease of use.



## Installation

> If you already have HACS, I2C and File editor configured, you can skip to [The actual installation](#the-actual-installation)


#### Video tutorials

- [Install HACS video](https://youtu.be/Fl3lATWhQVM) for step 1.
- [Enable I2C and Install file editor video](https://youtu.be/53Zj8NofS7k) for steps 2. and 3.
- [Install and config card drivers video](https://youtu.be/yH2HKjm7j24) for steps 4. and 5. (replace SMioplus-ha with SMmultiio-ha)

#### Prerequirements

1. Install HACS
    - Follow the official [instructions](https://www.hacs.xyz/docs/use/download/download/)

2. Install and run HassOS I2C Configurator add-on
    - Install [HassOS I2C Configurator](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fadamoutler%2FHassOSConfigurator)
    - Select your profile from the buttom left corner and enable `Advanced mode` in User settings
    - In Settings, Add-ons, Add-on Store, search and install `HassOS I2C Configurator`
    - Disable `Protection mode`
    - Start the add-on

3. Install File editor add-on
    - In Settings, Add-ons, Add-on Store, search and install `File editor`
    - Enable `Show in sidebar`
(see multiple config options bellow)


### The actual installation

4. Install SMmultiio-ha from HACS
    - Open HACS (from the sidebar)
    - Click on the 3 dots in the top right corner and select `Custom repositories`
    - Repository is `SequentMicrosystems/SMmultiio-ha` and type is `Integration`
    - Once added, you can now search it in HACS menu and download it

5. Add SMmultiio config in configuration.yaml
    - In the sidebar, select `File editor` and start the add-on
    - Click the folder icon from the top left corner and edit `configuration.yaml`
    - At the end of the file append the SMmultiio config:
        ```yaml
        SMmultiio:
        ```
        > for more information, see [configuration.yaml](#configuration.yaml)
    - Save the file

6. Reboot system

7. Reboot system (yes, it must be done twice)



## configuration.yaml

`configuration.yaml` example:
```yaml
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

SMmultiio:
    # + optional configs
```

- Simple stack 0 config:

```yaml
SMmultiio:
```

- Specific stack config:

```yaml
SMmultiio:
    - stack: 2
```

- Multiple cards on different stack levels:

```yaml
SMmultiio:
    - stack: 0
    - stack: 2
    - stack: 3
```

- Only specific entities for different stack levels:

> !The following example is provided for illustrative purposes only and does NOT necessarily represent real entities!

```yaml
SMmultiio:
    - stack: 0
      relay_1:
      relay_3:
      opto_1:
        update_interval: 0.1
    - stack: 2
      relay:
        channels: "1,2,5"
      opto_cnt:
        chan_range: "2..6"
        update_interval: 1
```

[//]: # (__CUSTOM_README__ START)
[//]: # (__CUSTOM_README__ END)

### `configuration.yaml` entities

Possible entities:
```yaml
opto_in_1: -> opto_in_4:  (type: binary_sensor)
rtc_1: (type: datetime)
iout_1: -> iout_2:  (type: number)
motor_1: (type: number)
servo_1: -> servo_2:  (type: number)
uout_1: -> uout_2:  (type: number)
iin_1: -> iin_2:  (type: sensor)
rtd_res_1: -> rtd_res_2:  (type: sensor)
rtd_temp_1: -> rtd_temp_2:  (type: sensor)
uin_1: -> uin_2:  (type: sensor)
led_1: -> led_6:  (type: switch)
relay_1: -> relay_2:  (type: switch)
```

Entity options:
- `channels: "l,i,s,t"` (comma separated channel numbers)
- `chan_range: "start..end"` (specify inclusive channel range)
- `update_interval: seconds` (specify the update interval for `sensor` and `binary_sensor`, default **30s**)
- `update_interval: seconds` (specify the update interval for `datetime`(RTC), default **1s**)
- `internet_sync_interval: seconds` (specify the internet sync interval for `datetime`(RTC), default **60s**)



### Troubleshooting:

1. Enities show up in the overview but do not function correctly
    - Make sure the I2C was enabled correctly. You can check if I2C was initialized properly by running the HassOS I2C Configurator again and checking the logs.
