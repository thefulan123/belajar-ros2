#!/usr/bin/env bash
# run.sh — Jalankan minimal_node.py
#
# Cara pakai:
#   bash run.sh
#   atau:
#   chmod +x run.sh && ./run.sh

# Source ROS2 dulu (wajib)
source /opt/ros/humble/setup.bash

# Jalankan node
python3 minimal_node.py
