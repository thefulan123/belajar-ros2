=== Dasar ROS2 / config/ ===

Folder untuk file konfigurasi YAML.

Digunakan untuk menyimpan parameter node dalam format YAML
yang bisa di-load saat runtime via launch file.

Contoh isi file .yaml:
  node_name:
    ros__parameters:
      param_name: value
