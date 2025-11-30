# SafeHome Testing Template Prefill

이 파일은 `Implementation_and_Testing_template_v4 (1).docx`를 채울 때 그대로 붙여넣을 수 있는 초안을 제공합니다. 템플릿의 **Overview → Introduction/Goal → Class Diagrams** 섹션을 우선 채우고, 이후 테스트 케이스 표를 추가하세요.

## Overview / Introduction
- This document captures the implementation and testing assets for the SafeHome security system. The system integrates configuration, login, sensor management, camera management, alarm handling, and user interfaces (control panel + dashboard).
- Architecture references: SDS sequence/state/class diagrams (see `docs/SDS_document.docx`) and SRS requirements (see `docs/SRS_document.doc`), especially UC8/UC9/UC10/UC12–16 (arming/disarming/zones), UC19–25 (cameras), and login/lockout requirements.

## Goal
- Practice traceable implementation and testing across unit, integration, and system levels using pytest + coverage with branch metrics.
- Validate alignment with SRS/SDS for security functions (arming modes, login/lockout, intrusion alarm, camera access) and document results in the provided template format (test IDs, inputs, expected/actual, references).
- Achieve high branch coverage on safety mode management, sensor/camera controllers, configuration/login flows, and UI-driven control panel interactions.

## Class Diagrams
- Source: `docs/diagrams/safehome_class_diagram.puml` (PlantUML).
- Contents: shows `System` orchestrating `ConfigurationManager`, `SensorController`, `CameraController`, `Alarm`; configuration stack (`DatabaseManager`, `StorageManager`, `SystemSettings`, `LoginManager`, `LogManager`, `SafetyZone`, `SafeHomeMode`); device stacks (Sensor + WindowDoorSensor/MotionSensor with hardware; CameraController + SafeHomeCamera + DeviceCamera; Alarm); interfaces (`SafeHomeControlPanel`, `LoginWindow`, `MainDashboard`).
- Insert into the template’s Class Diagram section by exporting the `.puml` to PNG/SVG (e.g., `plantuml docs/diagrams/safehome_class_diagram.puml`) and pasting the image. Keep the file path reference in the document for traceability.

## Next sections to fill in the DOCX
- Unit tests: one per public method in controllers/config/login/alarm/device wrappers; include SDS/SRS references (page numbers / UC IDs).
- Integration tests: flows like system-side login (System+LoginManager+StorageManager), arming with open windows/doors, camera access with/without passwords.
- System tests: end-to-end CP login + arm/disarm + alarm path; dashboard-driven camera PTZ + sensor simulator interactions.
- Branch coverage: use `coverage run --branch -m pytest` and `coverage report -m`, then paste file/class/method coverage numbers into the template tables.
