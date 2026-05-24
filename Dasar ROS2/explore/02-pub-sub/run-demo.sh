#!/usr/bin/env bash
# run-demo.sh — Jalankan talker + listener DALAM 2 TERMINAL
#
# Script ini membuka 2 jendela terminal:
#   Kiri:  talker (publisher)
#   Kanan: listener (subscriber)
#
# Ini membutuhkan terminal yang mendukung splitting.
# Kalau tidak bisa, jalankan manual di 2 terminal terpisah.

echo "=========================================="
echo "  ROS2 Publisher-Subscriber Demo"
echo "=========================================="
echo ""
echo "Buka 2 terminal dan jalankan:"
echo ""
echo "  Terminal 1:"
echo "    source /opt/ros/humble/setup.bash"
echo "    python3 talker.py"
echo ""
echo "  Terminal 2:"
echo "    source /opt/ros/humble/setup.bash"
echo "    python3 listener.py"
echo ""
echo "Atau kalau pakai gnome-terminal:"
gnome-terminal --tab -- bash -c "source /opt/ros/humble/setup.bash; python3 talker.py; exec bash" \
               --tab -- bash -c "sleep 1; source /opt/ros/humble/setup.bash; python3 listener.py; exec bash" 2>/dev/null || \
echo "gnome-terminal tidak tersedia. Jalankan manual."
