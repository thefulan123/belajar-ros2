# MODUL 10: Topic, Publisher, dan Subscriber

**TAG:** komunikasi / dasar / pub-sub

---

## APA ITU TOPIC?

Topic adalah **jalur komunikasi** antar node. Bayangkan topic sebagai:

> **Papan pengumuman** — siapa pun bisa menempel pengumuman,
> siapa pun bisa membaca pengumuman.

```
Publisher ──► Topic ──► Subscriber
(Pengirim)    (Papan)    (Penerima)
```

---

## APA ITU PUBLISHER DAN SUBSCRIBER?

| Peran | Fungsi | Analogi |
|-------|--------|---------|
| **Publisher** | Node yang **mengirim** data ke topic | Orang yang nempel pengumuman |
| **Subscriber** | Node yang **menerima** data dari topic | Orang yang membaca pengumuman |
| **Topic** | Nama jalur komunikasi | Papan pengumuman |

### Satu Topic, Banyak Pelaku

```
Publisher A ──┐
              ├──► Topic /chatter ──► Subscriber X
Publisher B ──┘                    └──► Subscriber Y
                                    └──► Subscriber Z
```

- Satu topic bisa punya **banyak publisher**
- Satu topic bisa punya **banyak subscriber**
- Publisher dan subscriber **tidak saling kenal** (decoupled)

---

## KENAPA ADA?

### Masalah

Tanpa topic, node harus saling kenal:

```python
# Node A harus tahu persis node B
class NodeA:
    def kirim_data(self):
        node_b = NodeB()
        node_b.terima_data("hello")
```

Masalah:
- Node A dan B terikat erat (tight coupling)
- Kalau Node B ganti nama atau lokasi → Node A harus diedit
- Sulit nambah subscriber baru

### Solusi

Dengan topic:

```python
# Node A: cuma kirim ke topic
publisher.publish("hello")
# Tidak peduli siapa yang baca

# Node B: cuma baca dari topic
subscriber.callback(data)
# Tidak peduli siapa yang kirim
```

**Decoupled** — publisher dan subscriber independen.

---

## CARA KERJA

### Alur Data

```
Publisher Node                      Subscriber Node
      │                                   │
      │  publisher.publish(msg)           │
      ├────────────────────────────────►  │
      │        topic /chatter            │
      │                                   │
      │                          callback(msg) dipanggil
      │                                   │
      │  (terus jalan)           (proses data)
```

### Tipe Data (Message Type)

Setiap topic punya **tipe pesan** tertentu:

| Topic | Tipe Pesan | Data |
|-------|-----------|------|
| `/chatter` | `std_msgs/String` | Teks |
| `/suhu` | `std_msgs/Float32` | Angka desimal |
| `/cmd_vel` | `geometry_msgs/Twist` | Kecepatan robot |

### Queue Size

```python
self.create_publisher(String, 'chatter', 10)
#                                                ^
#                                                Queue size
```

Queue size = berapa pesan yang diantre jika subscriber lambat.
- `10` = antre maksimal 10 pesan
- Kalau penuh → pesan paling lama dibuang

### Callback Subscriber

Subscriber bekerja dengan **callback**:

```python
def listener_callback(self, msg):
    # Fungsi ini dipanggil OTOMATIS
    # setiap kali ada data masuk di topic
    print(f"Menerima: {msg.data}")
```

Kamu tidak pernah memanggil `listener_callback()` secara langsung.
ROS2 yang memanggilnya saat ada data. Ini **event-driven**.

---

## CONTOH

### Publisher

```python
from std_msgs.msg import String

class TalkerNode(Node):
    def __init__(self):
        super().__init__('talker_node')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.callback)

    def callback(self):
        msg = String()
        msg.data = "Halo ROS2!"
        self.pub.publish(msg)         # ← kirim ke topic
```

### Subscriber

```python
class ListenerNode(Node):
    def __init__(self):
        super().__init__('listener_node')
        self.sub = self.create_subscription(
            String, 'chatter', self.callback, 10
        )

    def callback(self, msg):           # ← dipanggil otomatis
        print(f"Menerima: {msg.data}")
```

### Melihat dengan CLI

```bash
# Lihat topic yang tersedia
ros2 topic list

# Lihat data mentah di topic
ros2 topic echo /chatter

# Info topic
ros2 topic info /chatter

# Bandwidth (kecepatan data)
ros2 topic bw /chatter
```

---

## COBA INI

**Eksperimen 1 — Buktikan decoupling:**

1. Jalankan publisher saja (tanpa subscriber) → tetap jalan, tetap publish
2. Jalankan subscriber → langsung mulai terima data
3. Matikan subscriber → publisher tetap jalan

**Kesimpulan:** Publisher tidak tergantung subscriber.

**Eksperimen 2 — Satu publisher, banyak subscriber:**

1. Jalankan 1 publisher (`talker.py`)
2. Jalankan 2 subscriber (`listener.py`) di 2 terminal
3. Keduanya menerima data yang sama

**Eksperimen 3 — CLI langsung:**
```bash
# Kirim data ke topic langsung dari terminal
ros2 topic pub /chatter std_msgs/msg/String "data: 'Test dari CLI'" --once
```

---

## TOPIC vs SERVICE vs ACTION

| Aspek | Topic | Service | Action |
|-------|-------|---------|--------|
| Arah | Satu arah | Request-response | Goal-feedback-result |
| Durasi | Terus-menerus | Sekali panggil | Bisa lama |
| Feedback | Tidak | Tidak | Ya |
| Decoupled | Ya | Tidak (client tunggu) | Ya |

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| Topic tidak muncul di list | Node belum publish | Tunggu timer pertama |
| Data tidak sampai | Nama topic beda | Pastikan nama topic sama persis |
| Queue penuh | Subscriber lambat | Naikkan queue size |
| `No module named std_msgs` | Belum source | `source /opt/ros/humble/setup.bash` |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 09** — Node (node adalah pelaku pub/sub)
- **Lanjut ke Modul 11** — Service (request-response)
- **Praktek: explore/02-pub-sub** — implementasi pub/sub
