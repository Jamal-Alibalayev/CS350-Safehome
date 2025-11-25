-- SafeHome Database Schema (SQLite3)
-- Based on SRS and SDS requirements

-- 1. SystemSettings Table
CREATE TABLE IF NOT EXISTS system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_password TEXT NOT NULL,
    guest_password TEXT,  -- Optional
    web_password_1 TEXT NOT NULL,
    web_password_2 TEXT NOT NULL,
    entry_delay INTEGER DEFAULT 300,      -- seconds (minimum 5 minutes = 300s)
    exit_delay INTEGER DEFAULT 45,        -- seconds
    alarm_duration INTEGER DEFAULT 180,   -- seconds
    system_lock_time INTEGER DEFAULT 300, -- seconds
    monitoring_phone TEXT,
    homeowner_phone TEXT,
    max_login_attempts INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. SafetyZones Table
CREATE TABLE IF NOT EXISTS safety_zones (
    zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT NOT NULL,
    is_armed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SafeHomeModes Table
CREATE TABLE IF NOT EXISTS safehome_modes (
    mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode_name TEXT NOT NULL UNIQUE,  -- 'HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Sensors Table
CREATE TABLE IF NOT EXISTS sensors (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,        -- 'WINDOOR' or 'MOTION'
    sensor_location TEXT,
    zone_id INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES safety_zones(zone_id) ON DELETE SET NULL
);

-- 5. ModeSensorMapping Table (Mode and Sensor many-to-many relationship)
CREATE TABLE IF NOT EXISTS mode_sensor_mapping (
    mode_id INTEGER NOT NULL,
    sensor_id INTEGER NOT NULL,
    PRIMARY KEY (mode_id, sensor_id),
    FOREIGN KEY (mode_id) REFERENCES safehome_modes(mode_id) ON DELETE CASCADE,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

-- 6. Cameras Table
CREATE TABLE IF NOT EXISTS cameras (
    camera_id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_name TEXT,
    camera_location TEXT,
    camera_password TEXT,  -- Optional, can be NULL
    pan_angle INTEGER DEFAULT 0,
    zoom_level INTEGER DEFAULT 2,
    is_enabled BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. EventLogs Table (includes Intrusion Log)
CREATE TABLE IF NOT EXISTS event_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,         -- 'INFO', 'WARNING', 'ALARM', 'ERROR', 'INTRUSION'
    event_message TEXT NOT NULL,
    sensor_id INTEGER,
    camera_id INTEGER,
    zone_id INTEGER,
    source TEXT,                      -- 'System', 'Sensor', 'Camera', 'User'
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE SET NULL,
    FOREIGN KEY (camera_id) REFERENCES cameras(camera_id) ON DELETE SET NULL,
    FOREIGN KEY (zone_id) REFERENCES safety_zones(zone_id) ON DELETE SET NULL
);

-- 8. LoginSessions Table (tracks login attempts)
CREATE TABLE IF NOT EXISTS login_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    interface_type TEXT NOT NULL,     -- 'CONTROL_PANEL', 'WEB'
    username TEXT,
    login_successful BOOLEAN,
    failed_attempts INTEGER DEFAULT 0,
    login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_timestamp TIMESTAMP
);

-- Create indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_sensors_zone ON sensors(zone_id);
CREATE INDEX IF NOT EXISTS idx_sensors_type ON sensors(sensor_type);
CREATE INDEX IF NOT EXISTS idx_event_logs_timestamp ON event_logs(event_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_event_logs_type ON event_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_login_sessions_interface ON login_sessions(interface_type);

-- Insert default SafeHome modes
INSERT OR IGNORE INTO safehome_modes (mode_name, description) VALUES
    ('HOME', 'At home mode - partial sensors armed'),
    ('AWAY', 'Away mode - most sensors armed'),
    ('OVERNIGHT', 'Overnight travel mode'),
    ('EXTENDED', 'Extended travel mode - all sensors armed');

-- Insert default system settings
INSERT OR IGNORE INTO system_settings (
    id,
    master_password,
    web_password_1,
    web_password_2,
    monitoring_phone,
    homeowner_phone
) VALUES (
    1,
    '1234',           -- Default master password
    'webpass1',       -- Default web password 1
    'webpass2',       -- Default web password 2
    '911',            -- Default monitoring service phone
    '000-0000-0000'   -- Default homeowner phone
);
