from enum import Enum, auto

class SafeHomeMode(Enum):
    """
    定义系统的安防状态
    """
    DISARMED = auto()      # 撤防
    ARMED_AWAY = auto()    # 外出布防 (所有传感器激活)
    ARMED_STAY = auto()    # 在家布防 (通常只激活门窗，忽略内部动作)
    PANIC = auto()         # 紧急报警状态