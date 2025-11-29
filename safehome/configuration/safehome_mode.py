from enum import Enum, auto


class SafeHomeMode(Enum):
    """
    System security/arming status
    Defines different modes for the SafeHome system based on SRS requirements
    """

    # Basic modes
    DISARMED = auto()  # System disarmed, no sensors active

    # Arming modes (from SRS UC8, UC9, UC16)
    HOME = auto()  # Home mode - partial sensors armed (e.g., perimeter only)
    AWAY = auto()  # Away mode - most/all sensors armed
    OVERNIGHT = auto()  # Overnight travel mode
    EXTENDED = auto()  # Extended travel mode - maximum security

    # Legacy aliases for backward compatibility
    ARMED_STAY = auto()  # Alias for HOME mode
    ARMED_AWAY = auto()  # Alias for AWAY mode

    # Emergency mode
    PANIC = auto()  # Emergency panic state

    @classmethod
    def get_db_mode_name(cls, mode) -> str:
        """
        Convert enum mode to database mode name

        Args:
            mode: SafeHomeMode enum value

        Returns:
            String mode name for database (HOME, AWAY, OVERNIGHT, EXTENDED)
        """
        mapping = {
            cls.HOME: "HOME",
            cls.ARMED_STAY: "HOME",  # Legacy alias
            cls.AWAY: "AWAY",
            cls.ARMED_AWAY: "AWAY",  # Legacy alias
            cls.OVERNIGHT: "OVERNIGHT",
            cls.EXTENDED: "EXTENDED",
            cls.DISARMED: "DISARMED",
            cls.PANIC: "PANIC",
        }
        return mapping.get(mode, "DISARMED")

    @classmethod
    def from_db_mode_name(cls, mode_name: str):
        """
        Convert database mode name to enum

        Args:
            mode_name: Database mode name string

        Returns:
            SafeHomeMode enum value
        """
        mapping = {
            "HOME": cls.HOME,
            "AWAY": cls.AWAY,
            "OVERNIGHT": cls.OVERNIGHT,
            "EXTENDED": cls.EXTENDED,
            "DISARMED": cls.DISARMED,
            "PANIC": cls.PANIC,
        }
        return mapping.get(mode_name.upper(), cls.DISARMED)
