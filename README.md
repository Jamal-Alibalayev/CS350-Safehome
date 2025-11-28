# CS350-Safehome

## Alan's Branch
## note: 
1. the current comment is in chinese 

2. file structure
```
└─CS350-Safehome
    │  camera1.jpg
    │  README.md
    │  run_simulation.py                # simulation file for testing
    │  safehome_config.json             # config file
    │  safehome_events.log
    │
    ├─safehome
    │  ├─configuration
    │  │      configuration_manager.py
    │  │      log.py
    │  │      login_interface.py
    │  │      login_manager.py
    │  │      log_manager.py
    │  │      safehome_mode.py
    │  │      safety_zone.py
    │  │      storage_manager.py
    │  │      system_settings.py
    │  │
    │  ├─device
    │  │  │  __init__.py
    │  │  │
    │  │  ├─alarm                       # will be implement later
    │  │  ├─camera
    │  │  │      device_camera.py
    │  │  │      interface_camera.py
    │  │  │
    │  │  └─sensor
    │  │          device_motion_detector.py
    │  │          device_sensor_tester.py
    │  │          device_windoor_sensor.py
    │  │          interface_sensor.py
    │  │          safehome_sensor_test.py
    │  │          safehome_sensor_test_gui.py
    │  │
    │  └─interface
    │          camera_monitor.py
    │          device_control_panel_abstract.py
    │          safehome_control_panel.py
    │
    ├─test
    │      test_configuration.py        # unittest for configuration
    │
    └─virtual_device_v3                 # API provied by prof + sample code
        └─virtual_device_v3
            │  .DS_Store
            │  camera1.jpg
            │  camera2.jpg
            │  camera3.jpg
            │  floorplan.png
            │  README.md
            │  README.pdf
            │  requirements.txt
            │
            ├─device
            │      device_camera.py
            │      device_control_panel_abstract.py
            │      device_motion_detector.py
            │      device_sensor_tester.py
            │      device_windoor_sensor.py
            │      interface_camera.py
            │      interface_sensor.py
            │      safehome_sensor_test.py
            │      safehome_sensor_test_gui.py
            │      __init__.py
            │
            ├─example
            │  │  example_all_sensors.py
            │  │  example_camera.py
            │  │  example_control_panel.py
            │  │  __init__.py
            │  │
            │  └─__pycache__
            │          example_camera.cpython-311.pyc
            │          __init__.cpython-311.pyc
            │
            └─img
                    camera.png
                    control_panel.png
                    sensor.png
```
# User Manual
[User Manual](USER_MANUAL.md)