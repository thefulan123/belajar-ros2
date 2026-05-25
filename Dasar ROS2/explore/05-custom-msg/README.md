# explore/05-custom-msg — Custom Message

## Tujuan

Memahami bagaimana membuat dan menggunakan tipe pesan sendiri di ROS2:
- Custom message sebagai Python class (eksplorasi)
- Custom message sebagai .msg file (cara ROS2 yang benar)
- Serialisasi dan deserialisasi

## Cara Jalankan (Python-only demo)

Buka **2 terminal**:

```bash
# Terminal 1 — Publisher
source /opt/ros/humble/setup.bash
python3 pub_custom.py

# Terminal 2 — Subscriber
source /opt/ros/humble/setup.bash
python3 sub_custom.py
```

## Output

**Terminal 1:**
```
[INFO] Publisher custom message siap!
[INFO] Mengirim: SensorData(temp=28.5C, hum=65.0%, press=1013.2hPa)
[INFO] Mengirim: SensorData(temp=31.2C, hum=72.1%, press=1008.5hPa)
[INFO] Mengirim: SensorData(temp=33.8C, hum=55.3%, press=1011.9hPa)
```

**Terminal 2:**
```
[INFO] Subscriber custom message siap!
[INFO] Menerima: SensorData(temp=28.5C, hum=65.0%, press=1013.2hPa)
[WARN] Suhu tinggi! 31.2°C
[WARN] Suhu tinggi! 33.8°C
```

## Cara ROS2 yang Benar (dengan .msg + colcon)

1. Buat package baru:
   ```bash
   cd src
   ros2 pkg create --build-type ament_python sensor_msg_pkg
   ```

2. Buat folder `msg/`, simpan `SensorData.msg` (sudah disediakan)

3. Build:
   ```bash
   colcon build
   source install/setup.bash
   ```

4. Gunakan di code:
   ```python
   from sensor_msg_pkg.msg import SensorData
   msg = SensorData()
   msg.temperature = 28.5
   ```

## Coba Ini

1. **Edit my_custom_msg.py** — tambah field baru (contoh: `wind_speed`)
2. **Ubah threshold suhu** di `sub_custom.py` — ganti `30.0` jadi angka lain
3. **Cek topic**: `ros2 topic echo /sensor_data` — lihat data mentah (JSON string)

## Hubungan dengan Modul

- [Modul 12: Custom Interfaces](../../modul/12-custom-interfaces.md) — .msg, .srv, .action buatan sendiri
