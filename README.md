# CS350-Safehome

## Alan's Branch
## note: 
1. the current comment is in chinese 

2. file structure

└─CS350-Safehome
    │  camera1.jpg
    │  README.md
    │  run_simulation.py
    │  safehome_config.json
    │  safehome_events.log
    │
    ├─device
    │  │  device_camera.py
    │  │  device_control_panel_abstract.py
    │  │  device_motion_detector.py
    │  │  device_sensor_tester.py
    │  │  device_windoor_sensor.py
    │  │  interface_camera.py
    │  │  interface_sensor.py
    │  │  safehome_sensor_test.py
    │  │  safehome_sensor_test_gui.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          device_camera.cpython-313.pyc
    │          device_control_panel_abstract.cpython-313.pyc
    │          device_motion_detector.cpython-313.pyc
    │          device_sensor_tester.cpython-313.pyc
    │          device_windoor_sensor.cpython-313.pyc
    │          interface_camera.cpython-313.pyc
    │          interface_sensor.cpython-313.pyc
    │          safehome_sensor_test_gui.cpython-313.pyc
    │          __init__.cpython-313.pyc
    │
    ├─interface
    │  │  camera_monitor.py
    │  │  safehome_control_panel.py
    │  │
    │  └─__pycache__
    │          camera_monitor.cpython-313.pyc
    │          safehome_control_panel.cpython-313.pyc
    │
    ├─safehome
    │  └─configuration
    │      │  configuration_manager.py
    │      │  log.py
    │      │  login_interface.py
    │      │  login_manager.py
    │      │  log_manager.py
    │      │  safehome_mode.py
    │      │  safety_zone.py
    │      │  storage_manager.py
    │      │  system_settings.py
    │      │
    │      └─__pycache__
    │              configuration_manager.cpython-311.pyc
    │              configuration_manager.cpython-313.pyc
    │              log.cpython-311.pyc
    │              log.cpython-313.pyc
    │              login_interface.cpython-311.pyc
    │              login_interface.cpython-313.pyc
    │              login_manager.cpython-311.pyc
    │              login_manager.cpython-313.pyc
    │              log_manager.cpython-311.pyc
    │              log_manager.cpython-313.pyc
    │              safehome_mode.cpython-311.pyc
    │              safehome_mode.cpython-313.pyc
    │              safety_zone.cpython-311.pyc
    │              safety_zone.cpython-313.pyc
    │              storage_manager.cpython-311.pyc
    │              storage_manager.cpython-313.pyc
    │              system_settings.cpython-311.pyc
    │              system_settings.cpython-313.pyc
    │
    ├─test
    │      test_configuration.py
    │
    ├─virtual_device_v3
    │  ├─virtual_device_v3
    │  │  │  .DS_Store
    │  │  │  camera1.jpg
    │  │  │  camera2.jpg
    │  │  │  camera3.jpg
    │  │  │  floorplan.png
    │  │  │  README.md
    │  │  │  README.pdf
    │  │  │  requirements.txt
    │  │  │
    │  │  ├─device
    │  │  │  │  device_camera.py
    │  │  │  │  device_control_panel_abstract.py
    │  │  │  │  device_motion_detector.py
    │  │  │  │  device_sensor_tester.py
    │  │  │  │  device_windoor_sensor.py
    │  │  │  │  interface_camera.py
    │  │  │  │  interface_sensor.py
    │  │  │  │  safehome_sensor_test.py
    │  │  │  │  safehome_sensor_test_gui.py
    │  │  │  │  __init__.py
    │  │  │  │
    │  │  │  └─__pycache__
    │  │  │          device_camera.cpython-313.pyc
    │  │  │          device_control_panel_abstract.cpython-313.pyc
    │  │  │          device_motion_detector.cpython-313.pyc
    │  │  │          device_sensor_tester.cpython-313.pyc
    │  │  │          device_windoor_sensor.cpython-313.pyc
    │  │  │          interface_camera.cpython-313.pyc
    │  │  │          interface_sensor.cpython-313.pyc
    │  │  │          safehome_sensor_test_gui.cpython-313.pyc
    │  │  │          __init__.cpython-313.pyc
    │  │  │
    │  │  ├─example
    │  │  │  │  example_all_sensors.py
    │  │  │  │  example_camera.py
    │  │  │  │  example_control_panel.py
    │  │  │  │  __init__.py
    │  │  │  │
    │  │  │  └─__pycache__
    │  │  │          example_camera.cpython-311.pyc
    │  │  │          __init__.cpython-311.pyc
    │  │  │
    │  │  └─img
    │  │          camera.png
    │  │          control_panel.png
    │  │          sensor.png
    │  │
    │  └─__MACOSX
    │      │  ._virtual_device_v3
    │      │
    │      └─virtual_device_v3
    │          │  ._.DS_Store
    │          │  ._camera1.jpg
    │          │  ._camera2.jpg
    │          │  ._camera3.jpg
    │          │  ._device
    │          │  ._example
    │          │  ._floorplan.png
    │          │  ._img
    │          │  ._README.md
    │          │  ._README.pdf
    │          │  ._requirements.txt
    │          │
    │          ├─device
    │          │      ._device_camera.py
    │          │      ._device_control_panel_abstract.py
    │          │      ._device_motion_detector.py
    │          │      ._device_sensor_tester.py
    │          │      ._device_windoor_sensor.py
    │          │      ._interface_camera.py
    │          │      ._interface_sensor.py
    │          │      ._safehome_sensor_test.py
    │          │      ._safehome_sensor_test_gui.py
    │          │      .___init__.py
    │          │
    │          ├─example
    │          │      ._example_all_sensors.py
    │          │      ._example_camera.py
    │          │      ._example_control_panel.py
    │          │      .___init__.py
    │          │
    │          └─img
    │                  ._camera.png
    │                  ._control_panel.png
    │                  ._sensor.png
    │
    └─__pycache__
            safehome_control_panel.cpython-313.pyc