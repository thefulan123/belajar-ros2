#!/usr/bin/env bash

echo "=========================================="
echo "  ROS2 Action Demo (Fibonacci)"
echo "=========================================="
echo ""
echo "Buka 2 terminal:"
echo ""
echo "  Terminal 1 (server):"
echo "    source /opt/ros/humble/setup.bash"
echo "    python3 action_server.py"
echo ""
echo "  Terminal 2 (client):"
echo "    source /opt/ros/humble/setup.bash"
echo "    python3 action_client.py"

gnome-terminal --tab -- bash -c "source /opt/ros/humble/setup.bash; python3 action_server.py; exec bash" \
               --tab -- bash -c "sleep 2; source /opt/ros/humble/setup.bash; python3 action_client.py; exec bash" 2>/dev/null || \
echo "gnome-terminal tidak tersedia. Jalankan manual."
