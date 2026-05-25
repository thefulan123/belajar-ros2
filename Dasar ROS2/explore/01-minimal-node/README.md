# explore/01-minimal-node — Node ROS2 Pertama

## Tujuan

Membuat node ROS2 paling sederhana untuk memahami:
- Apa itu node
- Bagaimana cara membuat node
- Apa itu timer dan callback
- Bagaimana cara menjalankan node

## Cara Jalankan

```bash
# Terminal 1
source /opt/ros/humble/setup.bash
python3 minimal_node.py
```

## Output yang Diharapkan

```
[INFO] [....] Node minimal_node sudah hidup!
[INFO] [....] Halo dari node ROS2!
[INFO] [....] Halo dari node ROS2!
[INFO] [....] Halo dari node ROS2!
... (tiap 1 detik)
```

## Coba Ini

1. **Ganti pesan** — Edit `callback_timer`, ubah string di `get_logger().info()`
2. **Ganti kecepatan** — Edit `create_timer(1.0, ...)` jadi `0.5` atau `2.0`
3. **Cek dengan CLI** — Di terminal lain: `ros2 node list` (harusnya muncul `minimal_node`)
4. **Matikan** — Ctrl+C untuk berhenti

## Hubungan dengan Modul

- [Modul 03: Node](../../modul/03-node.md) — konsep node ROS2
- [Modul 10: Callback & Timer](../../modul/10-callback-timer.md) — callback dan timer periodik
