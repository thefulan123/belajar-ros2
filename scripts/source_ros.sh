#!/usr/bin/env bash
# ============================================================
# source_ros.sh — Aktifkan ROS2 Humble + workspace lokal
#
# Kenapa file ini ada?
# ROS2 perlu di-"source" setiap kali buka terminal baru.
# Command: source /opt/ros/humble/setup.bash
# Tapi hafalin path panjang itu gak perlu.
# File ini biar kamu cukup ketik:
#   source scripts/source_ros.sh
#
# Cara pakai:
#   1. Buka terminal
#   2. source scripts/source_ros.sh
#   3. Cek: ros2 --version
#
# Catatan:
# - Wajib pakai "source", bukan bash.
#   "source" = jalankan di terminal saat ini.
#   "bash"   = jalankan di sub-shell, ROS2 gak ke-detect.
# ============================================================

# Cek apakah ROS2 Humble ada
if [ ! -f "/opt/ros/humble/setup.bash" ]; then
    echo " ROS2 Humble tidak ditemukan di /opt/ros/humble/"
    echo " Pastikan ROS2 sudah terinstall."
    echo " Panduan: https://docs.ros.org/en/humble/Installation.html"
    return 1
fi

# Source ROS2
source /opt/ros/humble/setup.bash

# Source workspace lokal (kalau sudah ada)
LOCAL_WS="/mnt/e/Learn ROS2 from Scratch/src"
if [ -f "$LOCAL_WS/install/setup.bash" ]; then
    source "$LOCAL_WS/install/setup.bash"
    echo " Workspace lokal: $LOCAL_WS"
fi

echo " ROS2 ${ROS_DISTRO} siap digunakan!"
echo " Coba ketik: ros2 --version"
