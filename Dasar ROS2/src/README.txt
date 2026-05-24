=== Dasar ROS2 / src/ ===

Track 2: ROS2 colcon workspace.

Berisi package ROS2 lengkap yang dibangun dengan colcon build.
Semua node digabung dalam satu package untuk simulasi sistem penuh.

Struktur:
  ros2_basics/          → Package utama
    ros2_basics/        → Python source code
      *.py              → 10 node ROS2 (talker, listener, service, action, dll)
    launch/             → Launch file untuk semua node
    resource/           → Resource marker
    package.xml         → Manifest package
    setup.py            → Setup script

  build/                → Output build (colcon)
  install/              → Hasil instalasi
  log/                  → Log build

Cara build:
  cd Dasar ROS2/src/
  colcon build

Cara jalankan:
  source install/setup.bash
  ros2 run ros2_basics talker_node
