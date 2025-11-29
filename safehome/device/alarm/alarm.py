import threading
import time
from typing import Optional


class Alarm:
    """
    Alarm hardware driver (simulation)
    Implements alarm control with automatic shutoff timer
    Based on SRS requirements for alarm activation (UC8, UC9, UC16)
    """

    def __init__(self, duration: int = 180):
        """
        Initialize Alarm

        Args:
            duration: Duration in seconds before auto-shutoff (default: 180s = 3 minutes)
        """
        self.duration = duration
        self.is_ringing = False
        self._alarm_thread: Optional[threading.Thread] = None

    def ring(self):
        """
        Trigger the alarm
        Starts alarm sound in separate thread with auto-shutoff
        """
        if self.is_ringing:
            # Alarm already ringing
            return

        self.is_ringing = True
        self._alarm_thread = threading.Thread(
            target=self._ring_for_duration, daemon=True
        )
        self._alarm_thread.start()

    def _ring_for_duration(self):
        """
        Internal method that runs in separate thread
        Rings alarm for specified duration then auto-stops
        """
        print("🚨 ALARM RINGING! 🚨")
        time.sleep(self.duration)
        self.stop()

    def stop(self):
        """
        Stop the alarm immediately
        """
        self.is_ringing = False
        print("🔇 Alarm stopped.")

    def is_active(self) -> bool:
        """
        Check if alarm is currently ringing

        Returns:
            True if alarm is active, False otherwise
        """
        return self.is_ringing

    def set_duration(self, duration: int):
        """
        Set alarm duration

        Args:
            duration: Duration in seconds
        """
        self.duration = duration

    def get_duration(self) -> int:
        """
        Get current alarm duration setting

        Returns:
            Duration in seconds
        """
        return self.duration

    def get_status(self) -> dict:
        """
        Get alarm status as dictionary

        Returns:
            Dictionary with alarm status information
        """
        return {
            "is_ringing": self.is_ringing,
            "duration": self.duration,
            "has_active_thread": self._alarm_thread is not None
            and self._alarm_thread.is_alive(),
        }

    def __repr__(self):
        return f"Alarm(ringing={self.is_ringing}, duration={self.duration}s)"
