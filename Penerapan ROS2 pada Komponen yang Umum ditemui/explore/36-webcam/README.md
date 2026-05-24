# explore/36-webcam — Webcam via ROS2 (PC-side)

## Tujuan

Belajar **Publisher gambar** — membaca webcam dan publish ke ROS2 sebagai image topic.

Berbeda dengan explore lain — ini **PC-side only** (tidak pakai Arduino/micro-ROS).

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (PC) |
| Topic | `/webcam` |
| Tipe | `sensor_msgs/Image` |
| Frekuensi | ~15 FPS |

## Prasyarat

```bash
pip3 install opencv-python
pip3 install sensor_msgs_py  # (biasanya sudah include di ROS2)
```

## Cara Jalankan

### 1. Jalankan node webcam
```bash
source /opt/ros/humble/setup.bash
python3 webcam_node.py
```

### 2. Lihat gambar
```bash
# Cek apakah topic ada
ros2 topic list

# Lihat pakai image viewer
ros2 run rqt_image_view rqt_image_view
# Pilih topic /webcam
```

## Coba Ini

1. **Deteksi wajah:** Integrasi dengan OpenCV Haar Cascade
2. **Object tracking:** Track benda berwarna, publish koordinat
3. **Motion detection:** Jika ada perubahan frame, publish Bool ke /gerakan
4. **Integrasi MPU6050 (explore/17):** Stabilisasi kamera dengan data gyro
