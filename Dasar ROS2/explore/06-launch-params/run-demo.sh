#!/usr/bin/env bash

echo "=========================================="
echo "  ROS2 Launch File + Parameter Demo"
echo "=========================================="
echo ""
echo "  Opsi 1: Node standalone"
echo "    python3 param_node.py"
echo ""
echo "  Opsi 2: Node dengan parameter CLI"
echo '    python3 param_node.py --ros-args -p publish_rate:=0.5 -p max_count:=5'
echo ""
echo "  Opsi 3: Launch file (2 node)"
echo "    ros2 launch launch/param_demo.launch.py"
echo ""

# Jalankan opsi 3 via gnome-terminal kalau ada
gnome-terminal -- bash -c "
  source /opt/ros/humble/setup.bash
  cd $(dirname "$0")
  echo 'Menjalankan launch file...'
  ros2 launch launch/param_demo.launch.py
  exec bash
" 2>/dev/null || echo "gnome-terminal tidak tersedia."
