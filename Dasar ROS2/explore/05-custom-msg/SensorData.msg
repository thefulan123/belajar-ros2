# SensorData.msg — Definisi Custom Message ROS2
#
# Cara pakai:
#   1. Buat package ROS2: ros2 pkg create --build-type ament_python sensor_msg_pkg
#   2. Buat folder msg/ di dalam package
#   3. Simpan file ini di msg/SensorData.msg
#   4. Update package.xml: <depend>rosidl_defaultgenerators</depend>
#   5. Update setup.py: tambah dari rosidl_defaultgenerators import ...
#   6. colcon build
#   7. Import: from sensor_msg_pkg.msg import SensorData
#
# Format .msg:
# - Satu baris = satu field
# - Tipe data: float32, int32, string, bool, dll
# - Bisa juga nested: sensor_msg_pkg/OtherMsg field_name

float32 temperature
float32 humidity
float32 pressure
string unit
