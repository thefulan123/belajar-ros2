# MODUL 03: Node

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

- **Sebelumnya: Modul 01-02** — environment + turtlesim (pengenalan ROS2)
- **Lanjut ke Modul 04** — Topic, Publisher, Subscriber (node ngobrol)
- **Praktek: explore/01-minimal-node** — node pertamamu
- **Penerapan Praktik:** Setiap [komponen penerapan](../../Penerapan%20ROS2%20pada%20Komponen%20yang%20Umum%20ditemui/explore/01-led/README.md) adalah ROS2 node — diawali `rclc_node_init_default()` di .ino
   Lihat [KORELASI.md](../docs/KORELASI.md) untuk mapping lengkap.

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie nulis kode di `setup()` + `loop()`. Di ROS2, kita buat **Node**.

### Arduino (setup + loop):
```cpp
void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
  delay(1000);
}
```
Program Arduino cuma punya 2 fungsi — semua kode masuk situ. Kalau makin besar, `loop()` jadi panjang dan campur aduk.

### ROS2 (Node):
```python
class LedNode(Node):
    def __init__(self):
        super().__init__('led_node')   # Nama node UNIK
        self.pub = self.create_publisher(...)
        self.sub = self.create_subscription(...)
        self.timer = self.create_timer(...)
```
Setiap "program" di ROS2 adalah **Node** dengan nama unik. Node bisa punya publisher, subscriber, timer, service — semua terorganisir rapi dalam 1 class.

| Aspek | ROS2 Node | Arduino setup() + loop() |
|-------|-----------|-------------------------|
| Struktur | Class Python/C++ — method terpisah | 2 fungsi: setup(), loop() |
| Identitas | Nama unik (contoh: `/led_node`) | Nggak ada — semua anonymous |
| Banyak program | 1 terminal = 1 node; bisa banyak | 1 Arduino = 1 program |
| Komunikasi | Node bisa "ngobrol" via topic/service | Serial.print() — manual, satu arah |
| Lifecycle | init → spin → shutdown | setup → loop → loop → ... |
| Cocok | Banyak komponen yang perlu koordinasi | Projekt tunggal, 1 board |

**Intinya:** Kalau Arduino `loop()` itu kayak buku catatan isinya campur aduk, ROS2 Node itu kayak rak buku terorganisir — setiap bagian punya tempat sendiri dan bisa ditemuin dengan mudah.

---

## 📁 PRAKTIK

Praktik ini menjalankan **node ROS2** dan melihatnya di daftar node.

### Langkah 1: Buka folder explore
```
cd Dasar ROS2/explore/01-minimal-node/
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

---

## REFERENSI

- [ROS2 Humble: Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [ROS2 Humble: Using parameters in a class (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
