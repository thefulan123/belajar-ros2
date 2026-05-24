# explore/04-action — Action Server & Client

## Tujuan

Memahami komunikasi **action** di ROS2:
- Action server: node yang menerima goal, mengirim feedback, mengembalikan result
- Action client: node yang mengirim goal, menerima feedback, menerima result
- Perbedaan action dengan topic dan service

## Action vs Topic vs Service

| Aspek | Topic | Service | Action |
|-------|-------|---------|--------|
| Arah | Satu arah | Request-response | Goal-feedback-result |
| Durasi | Terus-menerus | Sekali panggil | Bisa lama |
| Feedback | Tidak | Tidak | Ya (progress) |
| Cancel | Tidak | Tidak | Ya (bisa dibatalkan) |
| Contoh | Data sensor | Jumlahkan angka | Robot jalan ke titik |

## Cara Jalankan

Buka **2 terminal**:

```bash
# Terminal 1 — Action Server (jalankan DULU)
source /opt/ros/humble/setup.bash
python3 action_server.py

# Terminal 2 — Action Client
source /opt/ros/humble/setup.bash
python3 action_client.py
```

## Output yang Diharapkan

**Terminal 1 (server):**
```
[INFO] Action server /fibonacci siap!
[INFO] Menerima goal: Fibonacci ke-10
[INFO] Feedback: [0, 1, 1]
[INFO] Feedback: [0, 1, 1, 2]
[INFO] Feedback: [0, 1, 1, 2, 3]
...
[INFO] Selesai! Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

**Terminal 2 (client):**
```
[INFO] Action server ditemukan!
[INFO] Mengirim goal: Fibonacci ke-10
[INFO] Goal diterima oleh server!
[INFO] Feedback: [0, 1, 1]
[INFO] Feedback: [0, 1, 1, 2]
...
[INFO] Result akhir: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

## Coba Ini

### 1. Ganti urutan Fibonacci
Edit `action_client.py` — ubah `goal_msg.order` jadi angka lain (5, 20, dst)

### 2. Cek dengan CLI
```bash
# Di terminal lain:
source /opt/ros/humble/setup.bash
ros2 action list                    # Lihat action tersedia
ros2 action info /fibonacci         # Info action
```

### 3. Canceling
Action bisa di-cancel. Coba tekan Ctrl+C di server saat sedang proses.

## Hubungan dengan explore lain

- **explore/03-service**: service tanpa feedback — action punya feedback
- **explore/02**: topic (broadcast) vs action (goal-based)
