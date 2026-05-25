# MODUL 10: Callback, Event-Driven, dan Timer

**TAG:** pemrograman / konsep / arsitektur

---

## APA ITU CALLBACK?

Callback adalah fungsi yang dipanggil secara otomatis ketika sesuatu terjadi.

Dalam ROS2, callback dipanggil ketika:
- Ada data masuk dari topic (`subscriber callback`)
- Ada request dari client (`service callback`)
- Timer mencapai interval tertentu (`timer callback`)

---

## KENAPA ADA?

### Masalah

Coba bayangkan program biasa:
```python
print("Mulai")
x = input("Masukkan angka: ")  ← program berhenti di sini sampai user input
print("Selesai")
```

Program ini **bloking** — berhenti sampai ada input.

Sekarang bayangkan robot yang harus:
- Membaca sensor suhu tiap 100ms
- Mengirim data motor tiap 50ms
- Menunggu perintah dari remote control
- Merespon emergency stop

Kalau pakai input() biasa, robot cuma bisa melakukan **satu hal dalam satu waktu**.

### Solusi

**Event-Driven Programming** — program tidak berjalan linear, tapi **bereaksi** terhadap kejadian (event).

Program "tidur" sampai ada sesuatu terjadi:
- Timer mencapai waktunya → jalankan callback
- Data masuk dari topic → jalankan callback
- Service dipanggil → jalankan callback

---

## CARA KERJA

### Program Linear (Biasa)

```
mulai → ambil data → olah → simpan → kirim → ambil data lagi → ...
```

Program mengontrol kapan setiap langkah terjadi.

### Event-Driven (ROS2)

```
                    ┌── timer callback ──┐
                    │                     │
  data sensor ──────┤  subscriber cb     ├──── motor
                    │                     │
  service call ─────┤  service cb        │
                    └────────────────────┘
```

Program menunggu, lalu bereaksi ketika ada event.

### rclpy.spin()

```python
import rclpy
from rclpy.node import Node

class ContohNode(Node):
    def __init__(self):
        super().__init__('contoh')
        # Timer akan memanggil callback tiap 1 detik
        self.timer = self.create_timer(1.0, self.callback_timer)

    def callback_timer(self):
        # Fungsi ini dipanggil otomatis tiap 1 detik
        self.get_logger().info("Timer triggered!")

def main():
    rclpy.init()
    node = ContohNode()
    rclpy.spin(node)  # ← ini yang membuat program terus jalan
```

`rclpy.spin()` menjaga program tetap hidup dan menunggu event.

Tanpa `spin()`, program akan langsung selesai.

### Timer

Timer adalah event yang paling dasar:
```python
self.timer = self.create_timer(interval_detik, callback_fungsi)
```

| Parameter | Fungsi |
|-----------|--------|
| `interval_detik` | Waktu antar eksekusi (dalam detik, bisa float) |
| `callback_fungsi` | Fungsi yang dipanggil setiap interval |

Setiap interval terlewati, callback dipanggil otomatis.

### Callback Flow

```
Timer(1.0, callback)
     │
     ├── detik 1 ──→ callback() dijalankan
     │                print("Hello ROS2")
     │
     ├── detik 2 ──→ callback() dijalankan
     │                print("Hello ROS2")
     │
     └── detik 3 ──→ callback() dijalankan
                      print("Hello ROS2")
                      ... terus sampai program dihentikan
```

Callback = fungsi yang dipanggil otomatis oleh sistem, bukan oleh kode kita langsung.

---

## CONTOH

```python
import rclpy
from rclpy.node import Node

class TimerNode(Node):
    def __init__(self):
        super().__init__('timer_node')
        # Timer callback tiap 0.5 detik
        self.timer = self.create_timer(0.5, self.say_hello)
        self.counter = 0

    def say_hello(self):
        self.counter += 1
        self.get_logger().info(f"Halo {self.counter}")

def main():
    rclpy.init()
    node = TimerNode()
    rclpy.spin(node)  # Jaga program tetap hidup
```

Output:
```
[INFO] Halo 1
[INFO] Halo 2
[INFO] Halo 3
...
```

---

## COBA INI

**Eksperimen — Bedakan program linear vs event-driven:**

Buka Python REPL:
```python
# Program linear
import time
time.sleep(1)
print("Satu detik kemudian")  # ← bloking, tidak bisa ngapa-ngapain
```

Sekarang bandingkan dengan node ROS2 yang pakai timer callback — node bisa:
- Print hello tiap detik
- Sambil tetap siap menerima data dari topic
- Sambil tetap merespon service call

Semua terjadi "bersamaan" karena callback-based.

**Eksperimen — Hapus `rclpy.spin()`:**

```python
def main():
    rclpy.init()
    node = TimerNode()
    # Tanpa spin(), program selesai segera
    # node dibuat lalu dihancurkan
    # Timer tidak pernah sempat jalan
```

Coba jalankan tanpa `rclpy.spin()` — node akan langsung mati tanpa output.

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| Node mati tanpa output | Lupa `rclpy.spin()` | Tambahkan `rclpy.spin(node)` |
| Callback tidak pernah jalan | Timer tidak dibuat | Pastikan `create_timer()` dipanggil |
| Program tidak merespon exit | `spin()` berjalan terus | Tekan Ctrl+C |
| `get_logger` error | Node belum dibuat | Panggil setelah `super().__init__()` |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Modul 03** — Node (node adalah tempat callback berjalan)
- **Modul 04** — Topic (subscriber callback dari data topic)
- **Modul 05** — Service (service callback dari request client)
- **Praktek: explore/01-minimal-node** — node pertama dengan timer callback

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie biasanya pake `delay()` untuk ngatur waktu. Di ROS2, ada **timer callback**.

### Arduino (tanpa ROS2):
```cpp
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);           // ← BERHENTI. Nggak bisa ngapa-ngapain.
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);           // ← BERHENTI lagi.
}
```
**Masalah:** Selama `delay()`, Arduino **buta** — nggak bisa baca sensor, nggak bisa terima data.

### ROS2 (dengan timer callback):
```python
self.timer = self.create_timer(1.0, self.callback)
# ← Nggak bloking! Node tetep bisa nerima data dari topic lain.
```
**Kelebihan:** Node tetep "dengar" sambil nunggu timer — event-driven, bukan blocking.

| Aspek | ROS2 Timer Callback | Arduino delay() |
|-------|---------------------|-----------------|
| Bloking? | ❌ Tidak — callback jalan di background | ✅ Ya — program berhenti total |
| Multi-tasking | Bisa timer + subscriber + service barengan | Hanya 1 hal dalam 1 waktu |
| Fleksibilitas | Interval bisa float (0.5 detik, 0.01 detik) | delay(milliseconds) — integer |
| Berhenti kapan? | Program jalan sampai Ctrl+C | delay() selesai — lanjut ke baris berikut |
| Cara pikir | "Reaktif" — fungsi dipanggil kalau waktunya tiba | "Linear" — aku tidur dulu, bangun, lanjut |

**Intinya:** `delay()` itu kayak orang meditasi — nggak sadar sekitar. Timer callback kayak orang multitasking — ngerjain sesuatu sambil nunggu alarm.

---

## 📁 PRAKTIK

Praktik ini menjalankan node ROS2 dengan **timer callback** dari folder explore.

### Langkah 1: Buka folder explore
```
cd Dasar ROS2/explore/01-minimal-node/
```

### Langkah 2: Buka file kode
Buka file `minimal_node.py` untuk melihat isinya.

### Langkah 3: Buka terminal — jalankan node
```bash
source /opt/ros/humble/setup.bash
python3 minimal_node.py
```

### Output yang diharapkan:
```
[INFO] [....] [minimal_node]: Halo dari node ROS2 minimal_node
[INFO] [....] [minimal_node]: Halo dari node ROS2 minimal_node
[INFO] [....] [minimal_node]: Halo dari node ROS2 minimal_node
...
```

Pesan `Halo dari node ROS2 minimal_node` muncul **setiap 2 detik** — ini adalah hasil dari **timer callback**.

### Cara kerja:
1. `create_timer(2.0, callback)` membuat timer dengan interval 2 detik
2. Setiap 2 detik, fungsi `callback` dipanggil **otomatis**
3. `rclpy.spin(node)` menjaga program tetap berjalan dan menunggu event

### Berhenti:
Tekan **Ctrl+C** untuk menghentikan program.

**Kesimpulan:** Timer callback memungkinkan fungsi berjalan periodik tanpa bloking. Ini adalah fondasi event-driven programming di ROS2.

---

## REFERENSI

- [ROS2 Humble: Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [ROS2 Humble: Using callbacks groups](https://docs.ros.org/en/humble/Tutorials/Intermediate/Using-Callback-Groups.html)
