# explore/06-launch-params — Launch File & Parameter

## Tujuan

Memahami:
- **Parameter**: pengaturan node yang bisa diubah dari luar
- **Launch file**: cara menjalankan banyak node sekaligus

## Kenapa Parameter?

Bayangkan kamu punya robot dengan 3 sensor. Tanpa parameter:

```python
# Harus edit kode setiap ganti pengaturan
publish_rate = 1.0
sensor_name = "sensor_depan"
```

Dengan parameter:

```bash
# Ganti pengaturan tanpa edit kode
ros2 param set /sensor_node publish_rate 2.0
ros2 param set /sensor_node sensor_name "sensor_belakang"
```

## Kenapa Launch File?

Robot nyata punya banyak node. Tanpa launch file:
```
Terminal 1: python3 sensor_node.py
Terminal 2: python3 motor_node.py
Terminal 3: python3 camera_node.py
Terminal 4: python3 navigation_node.py
```

Dengan launch file:
```bash
# Satu command untuk semua
ros2 launch launch/robot.launch.py
```

## Cara Jalankan

### Cara 1 — Node standalone (parameter default)
```bash
source /opt/ros/humble/setup.bash
python3 param_node.py
```

### Cara 2 — Node dengan parameter dari CLI
```bash
source /opt/ros/humble/setup.bash
python3 param_node.py \
  --ros-args \
  -p publish_rate:=0.5 \
  -p max_count:=5
```

### Cara 3 — Launch file (dua node sekaligus)
```bash
source /opt/ros/humble/setup.bash
cd "Dasar ROS2/explore/06-launch-params"
ros2 launch launch/param_demo.launch.py
```

## Output yang Diharapkan

**Cara 3 (launch file):**
```
[robot_node] [INFO] Node dimulai: robot_node
[robot_node] [INFO] Publish rate: 0.5 detik
[robot_node] [INFO] [1/5] Robot sedang berjalan...
[robot_node] [INFO] [2/5] Robot sedang berjalan...
...
[sensor_node] [INFO] Node dimulai: sensor_node
[sensor_node] [INFO] [1/3] Membaca sensor...
```

## Coba Ini

### 1. Ubah parameter dari CLI
Setelah node jalan, di terminal lain:
```bash
source /opt/ros/humble/setup.bash
ros2 param list                    # Lihat semua parameter
ros2 param get /param_node message  # Lihat nilai parameter
ros2 param set /param_node max_count 15  # Ubah parameter
```

### 2. Buat launch file sendiri
Copy `param_demo.launch.py`, ubah parameter-nya, jalankan.

### 3. Cek dengan CLI
```bash
ros2 node list                     # Lihat node yang jalan
ros2 param describe /param_node publish_rate  # Detail parameter
```

## Hubungan dengan Modul

- [Modul 06: Parameter](../../modul/06-parameter.md) — konfigurasi node runtime
- [Modul 09: Launch](../../modul/09-launch.md) — menjalankan banyak node sekaligus
