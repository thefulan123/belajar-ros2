# explore/02-pub-sub — Publisher & Subscriber

## Tujuan

Memahami komunikasi node ROS2 melalui **topic**:
- Publisher: node yang mengirim data
- Subscriber: node yang menerima data
- Topic: jalur komunikasi antara node

## Cara Jalankan

Buka **2 terminal**:

```bash
# Terminal 1 — Publisher
source /opt/ros/humble/setup.bash
python3 talker.py

# Terminal 2 — Subscriber
source /opt/ros/humble/setup.bash
python3 listener.py
```

## Output yang Diharapkan

**Terminal 1 (talker):**
```
[INFO] Talker node sudah hidup!
[INFO] Mengirim: "Halo ROS2! Pesan ke-0"
[INFO] Mengirim: "Halo ROS2! Pesan ke-1"
[INFO] Mengirim: "Halo ROS2! Pesan ke-2"
...
```

**Terminal 2 (listener):**
```
[INFO] Listener node sudah hidup!
[INFO] Menerima: "Halo ROS2! Pesan ke-0"
[INFO] Menerima: "Halo ROS2! Pesan ke-1"
[INFO] Menerima: "Halo ROS2! Pesan ke-2"
...
```

## Coba Ini

### 1. Matikan subscriber
Jalankan talker saja (tanpa listener). Lihat publisher tetap jalan?  
Itulah **decoupling** — publisher dan subscriber tidak saling tergantung.

### 2. Dua subscriber
Buka 2 terminal listener. Keduanya akan menerima pesan yang sama.  
Topic bisa punya banyak subscriber.

### 3. Cek dengan CLI
Di terminal lain:
```bash
source /opt/ros/humble/setup.bash
ros2 topic list              # Lihat daftar topic
ros2 topic info /chatter     # Info topic
ros2 topic echo /chatter     # Lihat langsung data mentah
ros2 topic bw /chatter       # Bandwidth topic
```

### 4. Ganti pesan
Edit `talker.py` — ubah `msg.data` jadi string lain.

### 5. Ganti kecepatan
Edit `create_timer(1.0, ...)` di talker jadi `0.2` (5x per detik) atau `2.0`.

## Debugging

| Masalah | Solusi |
|---------|--------|
| Topic tidak muncul | Pastikan kedua node jalan dan source ROS2 sudah benar |
| Tidak ada output | Pastikan nama topic sama (talker dan listener harus same topic name) |
| `ModuleNotFoundError` | Jalankan `source /opt/ros/humble/setup.bash` dulu |

## Hubungan dengan Modul

- Baca [Modul 10: Callback & Timer](../../modul/10-callback-timer.md)  
  (subscriber callback di listener.py persis seperti yang dijelaskan)
