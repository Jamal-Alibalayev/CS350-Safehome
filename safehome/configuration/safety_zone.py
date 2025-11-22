class SafetyZone:
    """
    代表一个物理安全区域 (例如: 1楼, 客厅)
    用于将多个传感器分组管理。
    """
    def __init__(self, zone_id: int, name: str):
        self.zone_id = zone_id
        self.name = name
        self.sensors = []  # 存储该区域下的传感器ID列表

    def add_sensor(self, sensor_id: int):
        """将传感器 ID 添加到该区域"""
        if sensor_id not in self.sensors:
            self.sensors.append(sensor_id)
    
    def remove_sensor(self, sensor_id: int):
        """从该区域移除传感器 ID"""
        if sensor_id in self.sensors:
            self.sensors.remove(sensor_id)

    def __repr__(self):
        return f"SafetyZone(id={self.zone_id}, name='{self.name}', sensors={self.sensors})"