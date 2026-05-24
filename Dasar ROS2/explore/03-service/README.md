# explore/03-service — Service Server & Client

## Tujuan

Memahami komunikasi **service** (request-response) di ROS2:
- Service server: node yang menerima request dan mengembalikan response
- Service client: node yang mengirim request dan menerima response
- Perbedaan service dengan topic

## Service vs Topic

| Aspek | Topic | Service |
|-------|-------|---------|
| Arah | Satu arah (broadcast) | Dua arah (request-response) |
| Durasi | Terus-menerus | Sekali panggil |
| Client | Tidak tahu siapa penerima | Tahu siapa yang meresponse |
| Contoh | Data sensor | "Jumlahkan 2+3" |
| ROS2 command | `ros2 topic` | `ros2 service` |

## Cara Jalankan

Buka **2 terminal**:

```bash
# Terminal 1 — Service Server (jalankan DULU)
source /opt/ros/humble/setup.bash
python3 service_server.py

# Terminal 2 — Service Client
source /opt/ros/humble/setup.bash
python3 service_client.py
```

## Output yang Diharapkan

**Terminal 1 (server):**
```
[INFO] Service server /add_two_ints siap!
[INFO] Menerima request: 5 + 3
[INFO] Mengirim response: 8
```

**Terminal 2 (client):**
```
[INFO] Mengirim request: 5 + 3
[INFO] Response: 8
```

## Coba Ini

### 1. Ganti angka
Edit `service_client.py` — ubah `request.a` dan `request.b`, jalankan ulang.

### 2. Cek dengan CLI
```bash
# Di terminal lain, setelah server jalan:
source /opt/ros/humble/setup.bash
ros2 service list                    # Lihat service tersedia
ros2 service type /add_two_ints      # Lihat tipe service
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"
```

### 3. Jalankan client sebelum server
Coba jalankan `service_client.py` dulu sebelum `service_server.py`.
Lihat pesan: "Service /add_two_ints belum tersedia, menunggu..."
Ini karena service client menunggu sampai server siap.

### 4. Matikan server, panggil client
Server mati → client gagal karena tidak ada yang melayani.

## Hubungan dengan explore lain

- **explore/01**: node dasar (service client di sini juga pake node)
- **explore/02**: topic (beda konsep dengan service — topic broadcast, service request-response)
