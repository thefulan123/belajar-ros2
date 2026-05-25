#!/usr/bin/env python3
"""
Test dasar: verifikasi semua node dan modul bisa di-import tanpa error.

Cara jalankan:
    cd Dasar ROS2/src
    colcon build
    source install/setup.bash
    python3 ../tests/test_imports.py

Atau dengan pytest:
    pip3 install pytest
    python3 -m pytest Dasar ROS2/tests/
"""

import sys
import os

# Tambahkan src/ ke path
SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
sys.path.insert(0, os.path.join(SRC_DIR, "ros2_basics"))


def test_talker_import():
    """Talker node bisa di-import."""
    from ros2_basics.talker_node import TalkerNode
    assert TalkerNode is not None


def test_listener_import():
    """Listener node bisa di-import."""
    from ros2_basics.listener_node import ListenerNode
    assert ListenerNode is not None


def test_service_server_import():
    """Service server node bisa di-import."""
    from ros2_basics.service_server_node import ServiceServerNode
    assert ServiceServerNode is not None


def test_service_client_import():
    """Service client node bisa di-import."""
    from ros2_basics.service_client_node import ServiceClientNode
    assert ServiceClientNode is not None


def test_action_server_import():
    """Action server node bisa di-import."""
    from ros2_basics.action_server_node import ActionServerNode
    assert ActionServerNode is not None


def test_action_client_import():
    """Action client node bisa di-import."""
    from ros2_basics.action_client_node import ActionClientNode
    assert ActionClientNode is not None


def test_param_node_import():
    """Parameter node bisa di-import."""
    from ros2_basics.param_node import ParamNode
    assert ParamNode is not None


def test_custom_msg_types():
    """Custom message types bisa di-import."""
    from ros2_basics.custom_msg_types import SensorData
    sensor = SensorData(temperature=25.0, humidity=60.0, pressure=1013.0)
    assert sensor.temperature == 25.0
    assert sensor.humidity == 60.0


def test_custom_pub_import():
    """Custom publisher node bisa di-import."""
    from ros2_basics.custom_pub_node import CustomPubNode
    assert CustomPubNode is not None


def test_custom_sub_import():
    """Custom subscriber node bisa di-import."""
    from ros2_basics.custom_sub_node import CustomSubNode
    assert CustomSubNode is not None


if __name__ == '__main__':
    # Run tests manually (tanpa pytest)
    tests = [
        ("TalkerNode", test_talker_import),
        ("ListenerNode", test_listener_import),
        ("ServiceServerNode", test_service_server_import),
        ("ServiceClientNode", test_service_client_import),
        ("ActionServerNode", test_action_server_import),
        ("ActionClientNode", test_action_client_import),
        ("ParamNode", test_param_node_import),
        ("SensorData", test_custom_msg_types),
        ("CustomPubNode", test_custom_pub_import),
        ("CustomSubNode", test_custom_sub_import),
    ]

    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
