import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Tuple, Any


class DatabaseManager:
    """
    SQLite3 Database Manager for SafeHome System
    Handles database connection, schema initialization, and query execution
    """

    def __init__(self, db_path: str = "data/safehome.db"):
        """
        Initialize Database Manager

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self._ensure_db_directory()

    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        """
        Connect to database

        Returns:
            sqlite3.Connection: Database connection object
        """
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,  # Allow multi-threaded access
                isolation_level=None,  # Enable autocommit mode
            )
            # Enable foreign key constraints
            self.connection.execute("PRAGMA foreign_keys = ON")
            # Return rows as dict-like objects
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize_schema(self):
        """
        Initialize database schema from schema.sql file
        Creates all tables and inserts default data
        """
        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r") as f:
            schema_sql = f.read()

        # Execute schema SQL
        cursor = self.connection.cursor()
        cursor.executescript(schema_sql)
        self.connection.commit()

    def execute_query(
        self,
        query: str,
        params: Tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False,
    ) -> Any:
        """
        Execute a SQL query

        Args:
            query: SQL query string
            params: Query parameters (tuple)
            fetch_one: If True, return one row
            fetch_all: If True, return all rows

        Returns:
            Query result (cursor, row, or rows)
        """
        if self.connection is None:  # Ensure connection is open before proceeding
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            # For non-SELECT queries, we might want the cursor itself
            # to get info like lastrowid, but we need a consistent return type.
            # We will return the cursor for legacy compatibility but encourage
            # using execute_insert_query for inserts.
            return cursor

    def execute_insert_query(self, query: str, params: Tuple = ()) -> Optional[int]:
        """
        Execute an INSERT SQL query and return the last inserted row ID.

        Args:
            query: SQL INSERT query string
            params: Query parameters (tuple)

        Returns:
            The ID of the last inserted row, or None if it fails.
        """
        if self.connection is None:
            self.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            return cursor.lastrowid
        except Exception as e:
            print(f"Error during insert query: {e}")
            return None

    def execute_many(self, query: str, params_list: List[Tuple]):
        """
        Execute a SQL query with multiple parameter sets

        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        cursor = self.connection.cursor()
        cursor.executemany(query, params_list)

    def commit(self):
        """Commit current transaction"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback current transaction"""
        if self.connection:
            self.connection.rollback()

    def get_last_insert_id(self) -> int:
        """
        Get the ID of the last inserted row

        Returns:
            int: Last insert row ID
        """
        cursor = self.connection.cursor()
        return cursor.lastrowid

    # ===== Convenience Methods =====

    def get_system_settings(self) -> Optional[sqlite3.Row]:
        """
        Get system settings (there should be only one row)

        Returns:
            System settings row or None
        """
        query = "SELECT * FROM system_settings WHERE id = 1"
        return self.execute_query(query, fetch_one=True)

    def update_system_settings(self, **kwargs):
        """
        Update system settings

        Args:
            **kwargs: Field-value pairs to update
        """
        if not kwargs:
            return

        # Build UPDATE query dynamically
        fields = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = tuple(kwargs.values())

        query = f"""
            UPDATE system_settings
            SET {fields}, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """
        self.execute_query(query, values)
        self.commit()

    def get_safety_zones(self) -> List[sqlite3.Row]:
        """Get all safety zones"""
        query = "SELECT * FROM safety_zones ORDER BY zone_id"
        return self.execute_query(query, fetch_all=True)

    def get_safehome_modes(self) -> List[sqlite3.Row]:
        """Get all SafeHome modes"""
        query = "SELECT * FROM safehome_modes ORDER BY mode_id"
        return self.execute_query(query, fetch_all=True)

    def get_sensors(self, zone_id: Optional[int] = None) -> List[sqlite3.Row]:
        """
        Get sensors, optionally filtered by zone

        Args:
            zone_id: If provided, return only sensors in this zone
        """
        if zone_id is not None:
            query = "SELECT * FROM sensors WHERE zone_id = ? ORDER BY sensor_id"
            return self.execute_query(query, (zone_id,), fetch_all=True)
        else:
            query = "SELECT * FROM sensors ORDER BY sensor_id"
            return self.execute_query(query, fetch_all=True)

    def get_cameras(self) -> List[sqlite3.Row]:
        """Get all cameras"""
        query = "SELECT * FROM cameras ORDER BY camera_id"
        return self.execute_query(query, fetch_all=True)

    def add_event_log(
        self,
        event_type: str,
        event_message: str,
        sensor_id: Optional[int] = None,
        camera_id: Optional[int] = None,
        zone_id: Optional[int] = None,
        source: str = "System",
    ) -> int:
        """
        Add an event log entry

        Returns:
            Log ID of inserted row
        """
        query = """
            INSERT INTO event_logs
            (event_type, event_message, sensor_id, camera_id, zone_id, source)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        last_id = self.execute_insert_query(
            query, (event_type, event_message, sensor_id, camera_id, zone_id, source)
        )
        self.commit()
        return last_id

    def get_event_logs(
        self,
        event_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
    ) -> List[sqlite3.Row]:
        """
        Get event logs with optional filters

        Args:
            event_type: Filter by event type
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Maximum number of rows to return

        Returns:
            List of log entries
        """
        query = "SELECT * FROM event_logs WHERE 1=1"
        params = []

        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)

        if start_date:
            query += " AND event_timestamp >= ?"
            params.append(start_date)

        if end_date:
            query += " AND event_timestamp <= ?"
            params.append(end_date)

        query += " ORDER BY event_timestamp DESC LIMIT ?"
        params.append(limit)

        return self.execute_query(query, tuple(params), fetch_all=True)

    def clear_event_logs(self):
        """Delete all event logs and seen markers."""
        # Remove seen markers first to maintain FK integrity if present
        try:
            self.execute_query("DELETE FROM event_log_seen")
        except Exception:
            pass
        self.execute_query("DELETE FROM event_logs")
        self.commit()

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.disconnect()
