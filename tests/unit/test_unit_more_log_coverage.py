from unittest.mock import MagicMock

import pytest

from safehome.configuration.log_manager import LogManager


def test_clear_logs_io_error(monkeypatch):
    """
    UT-LogMgr-ClearIOError: Test that an IOError during log file clearing is handled.
    测试 clear_logs 函数在清空日志文件时遇到IOError的异常处理能力。
    """
    # 模拟一个有db属性的存储管理器
    mock_storage = MagicMock()
    mock_storage.db = True

    lm = LogManager(storage_manager=mock_storage)

    # 使用 monkeypatch 使得 open 函数在被调用时抛出 IOError
    def mock_open(*args, **kwargs):
        raise IOError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    # 执行 clear_logs 并验证它没有因为IOError而崩溃
    try:
        lm.clear_logs()
    except IOError:
        pytest.fail("LogManager.clear_logs() should have handled the IOError.")

    # 验证即使文件操作失败，清空数据库的操作仍然被尝试调用
    mock_storage.clear_logs.assert_called_once()


def test_preload_logs_success():
    """
    UT-LogMgr-PreloadSuccess: Test successful preloading of logs from storage.
    测试 LogManager 初始化时从存储成功预加载日志。
    """
    # 准备一个包含日志数据的模拟存储管理器
    mock_storage = MagicMock()
    mock_storage.get_logs.return_value = [
        {
            "event_message": "System armed",
            "event_type": "SECURITY",
            "source": "MainPanel",
            "event_timestamp": "2023-10-27 10:00:00",
        },
        {
            "event_message": "Motion detected",
            "event_type": "WARNING",
            "source": "Living Room Sensor",
            "event_timestamp": "2023-10-27 10:05:00",
        },
    ]

    # 使用模拟存储来初始化 LogManager
    lm = LogManager(storage_manager=mock_storage)

    # 验证 get_logs 方法被调用
    mock_storage.get_logs.assert_called_with(limit=500)

    # 验证日志已成功加载到内存中
    all_logs = lm.get_all_logs()
    assert len(all_logs) == 2
    assert all_logs[0].message == "System armed"
    assert all_logs[1].source == "Living Room Sensor"
