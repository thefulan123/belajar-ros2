=== Dasar ROS2 / explore/ ===

Track 1: Standalone Python & Arduino files.

Setiap subfolder adalah proyek INDEPENDEN — bisa dijalankan sendiri
tanpa perlu build system. Cukup: python3 filename.py

Folder:
  01-minimal-node/     → Node ROS2 paling sederhana
  02-pub-sub/          → Publisher + Subscriber (topic)
  03-service/          → Service server + client
  04-action/           → Action server + client
  05-custom-msg/       → Custom message type
  06-launch-params/    → Launch file + parameter
  07-arduino-uno/      → micro-ROS dengan Arduino UNO

Cara pakai:
  cd 02-pub-sub/
  python3 talker.py    # terminal 1
  python3 listener.py  # terminal 2
