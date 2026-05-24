#!/usr/bin/env bash
# ============================================================
# run-agent.sh — Jalankan micro-ROS Agent untuk Arduino
#
# micro-ROS Agent adalah jembatan antara Arduino dan ROS2.
#
# Prasyarat:
#   1. micro-ROS agent sudah di-build (lihat modul 08)
#   2. Arduino terhubung via USB
#   3. Sketch sudah di-upload ke Arduino
#
# Cara pakai:
#   bash run-agent.sh                    # Auto-detect port
#   bash run-agent.sh /dev/ttyUSB0       # Manual port
# ============================================================

# Source ROS2
source /opt/ros/humble/setup.bash

# Source micro-ROS workspace (sesuaikan path jika berbeda)
MICROROS_WS="$HOME/microros_ws"
if [ -f "$MICROROS_WS/install/setup.bash" ]; then
    source "$MICROROS_WS/install/setup.bash"
fi

# Tentukan port serial
if [ -n "$1" ]; then
    SERIAL_PORT="$1"
else
    # Auto-detect: coba port yang umum
    if [ -e "/dev/ttyACM0" ]; then
        SERIAL_PORT="/dev/ttyACM0"
    elif [ -e "/dev/ttyUSB0" ]; then
        SERIAL_PORT="/dev/ttyUSB0"
    else
        echo "=========================================="
        echo "  ERROR: Arduino tidak ditemukan!"
        echo "=========================================="
        echo ""
        echo "  Colok Arduino dan cek port:"
        echo "    ls /dev/ttyACM* /dev/ttyUSB*"
        echo ""
        echo "  Lalu jalankan:"
        echo "    bash run-agent.sh /dev/port_anda"
        exit 1
    fi
fi

# Cek permission
if [ ! -r "$SERIAL_PORT" ]; then
    echo "=========================================="
    echo "  ERROR: Tidak punya akses ke $SERIAL_PORT"
    echo "=========================================="
    echo ""
    echo "  Solusi:"
    echo "    sudo chmod 666 $SERIAL_PORT"
    echo "    (atau) sudo usermod -aG dialout \$USER"
    echo "           lalu logout-login"
    exit 1
fi

# Jalankan agent
echo "=========================================="
echo "  micro-ROS Agent"
echo "=========================================="
echo ""
echo "  Port: $SERIAL_PORT"
echo "  Board: Arduino UNO"
echo "  Baud: 115200"
echo ""
echo "  Tekan Ctrl+C untuk berhenti"
echo "=========================================="
echo ""

ros2 run micro_ros_agent micro_ros_agent serial \
    --dev "$SERIAL_PORT" \
    --baud 115200
