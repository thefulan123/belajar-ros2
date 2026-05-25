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


---

## Modul Terkait

- [Dasar ROS2 Modul 03 — Node](../../Dasar%20ROS2/modul/03-node.md) — konsep node ROS2
- [Dasar ROS2 Modul 04 — Topic](../../Dasar%20ROS2/modul/04-topic-pub-sub.md) — komunikasi pub/sub
- [Dasar ROS2 Modul 10 — Callback & Timer](../../Dasar%20ROS2/modul/10-callback-timer.md) — callback & timer periodik
- [Dasar ROS2 Modul 11 — micro-ROS](../../Dasar%20ROS2/modul/11-micro-ros.md) — ROS2 di Arduino/ESP32
- [KORELASI.md](../../Dasar%20ROS2/docs/KORELASI.md) — mapping lengkap modul ↔ komponen

## 🔄 ROS2 vs Arduino Biasa

Webcam bisa dipake langsung dengan OpenCV + Python biasa. Tapi ROS2 ngasih lebih:

### Python biasa (OpenCV):
```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imshow("Camera", frame)
```
- Gambar cuma bisa dilihat di laptop sendiri
- Nggak bisa dikirim ke node lain

### ROS2 (sensor_msgs/Image):
```python
self.pub = self.create_publisher(Image, '/camera/image', 10)
self.pub.publish(msg)
```
- Gambar bisa dipake node lain (deteksi objek, log, streaming)
- Bisa digabung data sensor lain

### Perbandingan Langsung

| Aspek | ROS2 | OpenCV Biasa |
|-------|------|-------------|
| Data sampai ke | Seluruh sistem ROS2 | Hanya window lokal |
| Integrasi | Bisa digabung sensor, motor, dll | Standalone — sendiri |
| Expandability | Tinggal subscribe di node lain | Copy frame manual |
| Cocok | Robot vision, multi-sensor fusion | Tes kamera, face detection lokal |

