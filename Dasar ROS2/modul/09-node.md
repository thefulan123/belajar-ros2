# MODUL 09: Node

**TAG:** arsitektur / dasar / komponen utama

---

## APA ITU NODE?

Node adalah **unit terkecil** dalam sistem ROS2. Bayangkan node sebagai:

> Sebuah **program kecil** yang melakukan **satu tugas spesifik**.

Contoh dalam robot:
```
Robot
├── Node sensor_suhu     → membaca suhu
├── Node motor_kiri      → mengontrol motor kiri
├── Node motor_kanan     → mengontrol motor kanan
├── Node kamera          → mengambil gambar
├── Node navigasi        → menentukan arah
└── Node odometry        → menghitung posisi
```

---

## KENAPA ADA?

### Masalah

Bayangkan robot ditulis sebagai SATU program besar:

```python
# robot.py — satu program besar
while True:
    baca_sensor()
    proses_data()
    gerak_motor()
    kirim_data()
    ambil_gambar()
    # ... 1000 baris berikutnya
```

Masalahnya:
- Kalau error di sensor → seluruh robot mati
- Susah di-debug
- Susah ganti sensor (harus edit program besar)
- Tidak bisa重用 komponen

### Solusi

ROS2 membagi program menjadi **node-node kecil** yang independen:

```
Node sensor      Node motor        Node kamera
┌──────────┐    ┌──────────┐      ┌──────────┐
│  baca    │    │  gerak   │      │  ambil   │
│  sensor  │    │  motor   │      │  gambar  │
└──────────┘    └──────────┘      └──────────┘
     │               │                 │
     └───────────────┴─────────────────┘
                    │
              ROS2 Network
```

Keuntungan:
- **Modular** — ganti sensor = ganti satu node saja
- **Isolasi error** — sensor error, motor tetap jalan
- **重用** — node motor bisa dipakai di robot lain
- **Debug mudah** — lihat node mana yang error
- **Bahasa bebas** — node Python bisa ngobrol dengan node C++

---

## CARA KERJA

Setiap node di ROS2 punya:

| Komponen | Fungsi |
|----------|--------|
| **Nama** | Identifier unik (contoh: `sensor_node`) |
| **Publisher** | Mengirim data ke topic |
| **Subscriber** | Menerima data dari topic |
| **Service** | Menjawab request dari node lain |
| **Action** | Menangani task panjang dengan feedback |
| **Parameter** | Pengaturan yang bisa diubah tanpa edit kode |

### Node Minimal

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        # Nama node: 'minimal_node'
        # Nama ini muncul di: ros2 node list
        super().__init__('minimal_node')
        self.get_logger().info('Node hidup!')

def main():
    rclpy.init()          # 1. Nyalakan ROS2
    node = MinimalNode()  # 2. Buat node
    rclpy.spin(node)      # 3. Jaga node tetap hidup
    node.destroy_node()
    rclpy.shutdown()
```

Tanpa `rclpy.spin()`, node akan mati seketika.

### Satu Program, Banyak Node

Satu file Python bisa membuat banyak node:

```python
node1 = Node('node_pertama')
node2 = Node('node_kedua')
```

Tapi best practice: **satu node per file** — biar modular.

### Node di ROS2 vs Program Biasa

| Aspek | Program Biasa | ROS2 Node |
|-------|---------------|-----------|
| Eksekusi | Linear dari atas ke bawah | Event-driven (callback) |
| Komunikasi | Panggil fungsi langsung | Lewat topic/service |
| Sikap | Aktif (jalan terus) | Reaktif (menunggu event) |
| Error | Crash total | Hanya node itu saja |

---

## CONTOH

### Melihat Node yang Berjalan

```bash
# Terminal 1 — Jalankan node
source /opt/ros/humble/setup.bash
python3 "Dasar ROS2/explore/01-minimal-node/minimal_node.py"

# Terminal 2 — Lihat node
source /opt/ros/humble/setup.bash
ros2 node list
# Output: /minimal_node

# Info detail node
ros2 node info /minimal_node
# Output:
#   Subscribers: (none)
#   Publishers: (none)
#   Services: ...
#   Actions: ...
```

---

## COBA INI

**Eksperimen — Jalankan 2 node berbeda:**

1. Jalankan `minimal_node.py` di terminal 1
2. Jalankan `talker.py` (dari explore/02) di terminal 2
3. Di terminal 3: `ros2 node list`
   - Lihat ada 2 node: `/minimal_node` dan `/talker_node`

**Eksperimen — Ganti nama node:**
```python
super().__init__('nama_saya')
```
Jalankan ulang, cek `ros2 node list`.

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| Node tidak muncul di list | Belum source atau node mati | Pastikan `rclpy.spin()` ada |
| `rclpy not found` | Belum source ROS2 | `source /opt/ros/humble/setup.bash` |
| Node langsung mati | Lupa `rclpy.spin()` | Tambahkan `rclpy.spin(node)` |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 01-08** — infrastruktur ROS2
- **Lanjut ke Modul 10** — Topic, Publisher, Subscriber (node ngobrol)
- **Praktek: explore/01-minimal-node** — node pertamamu

---

## 📁 PRAKTIK

Praktik ini menjalankan **node ROS2** dan melihatnya di daftar node.

### Langkah 1: Buka folder explore
```
cd /mnt/e/Learn ROS2 from Scratch/Dasar ROS2/explore/01-minimal-node/
```

### Langkah 2: Buka file `minimal_node.py`
```python
class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')   # ← nama node
        self.timer = self.create_timer(2.0, self.callback)
```

Nama node adalah `minimal_node` — ini yang akan muncul di `ros2 node list`.

### Langkah 3: Terminal 1 — Jalankan node
```bash
source /opt/ros/humble/setup.bash
python3 minimal_node.py
```

### Langkah 4: Terminal 2 — Cek daftar node
```bash
source /opt/ros/humble/setup.bash
ros2 node list
```

**Output yang diharapkan:**
```
/minimal_node
```

### Langkah 5: Terminal 2 — Info node
```bash
ros2 node info /minimal_node
```

**Output yang diharapkan:**
```
/minimal_node
  Subscribers: []
  Publishers: []
  Services: []
  Action Servers: []
  Action Clients: []
```

**Kesimpulan:** Node `minimal_node` terdaftar di ROS2 graph dan bisa dideteksi dengan `ros2 node list`.
