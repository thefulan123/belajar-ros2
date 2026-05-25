# MODUL 07: Action

**TAG:** komunikasi / long-running / feedback

---

## APA ITU ACTION?

Action adalah komunikasi untuk **task yang berjalan lama** dengan **feedback** (laporan progress).

> Action = Service yang bisa **lapor progres** dan **dibatalkan**.

```
Client                         Server
  │                               │
  ├── goal (order=10) ──────────►│
  │                               │  Mulai proses
  │◄── feedback [0, 1, 1] ───────┤
  │◄── feedback [0, 1, 1, 2] ────┤  (setiap step)
  │◄── feedback [0,1,1,2,3] ─────┤
  │                               │  Selesai
  │◄── result [0,1,1,2,3,5,8] ───┤
```

---

## ACTION vs SERVICE vs TOPIC

| Aspek | Topic | Service | Action |
|-------|-------|---------|--------|
| Arah | Satu arah | Request-response | Goal-feedback-result |
| Feedback | Tidak | Tidak | **Ya** (progress) |
| Cancel | Tidak | Tidak | **Ya** |
| Durasi | Terus | Sekali | Bisa lama |
| Contoh | Data sensor | Reset odometry | Navigasi ke titik |
| Analogi | Radio | Telepon | Kurir paket (ada tracking) |

---

## KENAPA ADA?

### Masalah

Service cuma kasih response setelah selesai. Untuk tugas lama:

```python
# Service — client nunggu diam sampai selesai
response = client.call(request)  # Blok! Bisa 30 detik
```

Client tidak tahu progress. Tidak bisa cancel di tengah jalan.

### Contoh Masalah Nyata

Robot disuruh jalan ke titik tujuan (butuh 30 detik):

1. **Pakai service:** client mengirim request, lalu **diam menunggu** 30 detik.
   Tidak tahu robot sudah sampai mana.
   Tidak bisa bilang "berhenti di tengah jalan."

2. **Pakai action:** client mengirim goal, lalu **terima feedback** tiap detik:
   - "Sudah 10%"
   - "Sudah 50%"
   - Bisa cancel: "Berhenti!"
   - Dapat result saat sampai

### Solusi

Action memberikan tiga hal yang tidak dimiliki service:
1. **Feedback** — laporan progress selama proses
2. **Cancel** — batalkan tugas di tengah jalan
3. **Non-blocking** — client bisa melakukan hal lain sambil menunggu

---

## CARA KERJA

### Action Definition

```
# Fibonacci.action
int32 order        ← goal (input)
---
int32[] sequence   ← result (output akhir)
---
int32[] sequence   ← feedback (progress)
```

**Penting:** Ada 3 bagian dipisah `---`:
1. Goal (input)
2. Result (output akhir)
3. Feedback (progress)

### Server Side

```python
class ActionServerNode(Node):
    def __init__(self):
        super().__init__('action_server')
        self.action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',        # Nama action
            self.execute_callback
        )

    async def execute_callback(self, goal_handle):
        # goal_handle.request.order = input goal

        # Kirim feedback (progress)
        feedback = Fibonacci.Feedback()
        feedback.sequence = [0, 1]
        goal_handle.publish_feedback(feedback)

        # Cek cancel
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return Fibonacci.Result()

        # Selesai
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback.sequence
        return result
```

### Client Side

```python
class ActionClientNode(Node):
    def __init__(self):
        super().__init__('action_client')
        self.client = ActionClient(
            self, Fibonacci, 'fibonacci'
        )
        self.client.wait_for_server()

        # Kirim goal
        goal = Fibonacci.Goal()
        goal.order = 10
        self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_cb
        )

    def feedback_cb(self, feedback_msg):
        # Dipanggil setiap ada feedback dari server
        print(f"Progress: {feedback_msg.feedback.sequence}")

    def result_cb(self, future):
        result = future.result().result
        print(f"Selesai: {result.sequence}")
```

### Alur Lengkap

```
Client                              Server
  │                                    │
  │  send_goal_async(goal) ──────────►│  execute_callback mulai
  │                                    │
  │◄──────── feedback ────────────────┤  loop:
  │  (progress)                       │    publish_feedback()
  │                                    │
  │◄──────── feedback ────────────────┤
  │                                    │
  │  cancel_goal() ──────────────────►│  is_cancel_requested = True
  │◄──────── cancelled ──────────────┤
  │                                    │
  │  ATAU (kalau tidak di-cancel):    │
  │◄──────── result ─────────────────┤  succeed()
```

---

## CONTOH PENGGUNAAN NYATA

| Action | Fungsi |
|--------|--------|
| `/navigate_to_pose` | Robot jalan ke titik tujuan (feedback: jarak tersisa) |
| `/follow_path` | Robot ikuti jalur (feedback: waypoint saat ini) |
| `/pick_and_place` | Robot ambil dan pindahkan benda |
| `/scan_area` | Robot scan area (feedback: persentase selesai) |
| `/calibrate_sensor` | Kalibrasi sensor (feedback: status kalibrasi) |

---

## COBA INI

**Eksperimen 1 — Feedback real-time:**
```bash
python3 action_server.py  # Terminal 1
python3 action_client.py  # Terminal 2
```
Lihat feedback muncul setiap 0.5 detik.

**Eksperimen 2 — Cancel di tengah:**
1. Jalankan server + client
2. Saat feedback berjalan, tekan Ctrl+C di client
3. Lihat server menerima cancel request

**Eksperimen 3 — Ganti goal:**
Edit `action_client.py` — ubah `goal_msg.order = 5` atau `= 20`.
Semakin besar order, semakin lama proses (lihat feedback).

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `action server not available` | Lupa `wait_for_server()` | Tambahkan `wait_for_server()` |
| `goal_handle` error | Lupa `succeed()` | Panggil `goal_handle.succeed()` |
| Client hung selamanya | Feedback callback error | Cek `feedback_callback` tidak error |
| `action not found` | Nama action beda | Pastikan nama sama di server & client |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 05** — Service (action = service + feedback + cancel)
- **Sebelumnya: Modul 06** — Parameter (parameter digunakan untuk konfigurasi action)
- **Semua modul sebelumnya** — action memakai konsep node, callback, timer
- **Praktek: explore/04-action** — implementasi action

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie yang mau ngerjain tugas lama (misal: robot jalan 1 meter) harus bikin **state machine manual** pake loop + variable. Di ROS2, ada **Action**.

### Arduino (manual state machine):
```cpp
enum State {IDLE, MOVING, DONE};
State state = IDLE;
int progress = 0;

void loop() {
  switch(state) {
    case IDLE:
      if (Serial.available()) startMoving();
      break;
    case MOVING:
      // Jalan dikit, update progress
      progress++;
      Serial.print("Progress: "); Serial.println(progress);
      if (progress >= 10) state = DONE;
      break;
    case DONE:
      Serial.println("Selesai!");
      state = IDLE;
      break;
  }
}
```
**Masalah:** Kamu harus bikin state machine sendiri, ngirim feedback manual, handle cancel manual. Ribet.

### ROS2 (Action):
```python
# Action Server — otomatis handle goal, feedback, cancel
def execute_callback(self, goal_handle):
    for i in range(goal_handle.request.order):
        # Hitung, kirim feedback
        feedback_msg.sequence = sequence
        goal_handle.publish_feedback(feedback_msg)
        # Cek cancel
        if goal_handle.is_canceling():
            return Canceled()
    goal_handle.succeed()
    return result
```
Action udah punya **sistem goal-feedback-result-cancel** built-in. Kamu tinggal isi logic-nya.

| Aspek | ROS2 Action | Arduino Manual |
|-------|-------------|----------------|
| Goal | `send_goal(order)` — kirim tujuan | Variable global + switch case |
| Feedback | `publish_feedback()` — otomatis ke client | `Serial.print("Progress...")` — manual |
| Cancel | `goal_handle.is_canceling()` — deteksi otomatis | Flag variable — kamu atur sendiri |
| Result | `succeed()` + return | State machine manual |
| Multi-client | Bisa banyak client 1 server | Nggak bisa — 1 program, 1 state |
| Debug | `ros2 action list`, `ros2 action send_goal` | Serial Monitor — harus parsing sendiri |

**Intinya:** Action itu kayak **Gojek** — kamu pesan (goal), driver lapor posisi (feedback), sampe tujuan (result), bisa dibatalin (cancel). Arduino manual itu kayak **jalan kaki** — semua kamu atur sendiri: tujuan, progress, kapan berhenti.

---

## 📁 PRAKTIK

Praktik ini menjalankan **Action Server dan Client** ROS2 dari folder explore.

### Langkah 1: Buka folder explore
```
cd Dasar ROS2/explore/04-action/
```

Folder ini berisi dua file:
- `action_server.py` — node yang menjalankan **Fibonacci** secara bertahap
- `action_client.py` — node yang meminta Fibonacci dan menerima **feedback**

### Langkah 2: Terminal 1 — Jalankan action server
```bash
source /opt/ros/humble/setup.bash
python3 action_server.py
```

**Output yang diharapkan:**
```
[INFO] [....] [action_server_node]: Action server siap di /fibonacci
```

### Langkah 3: Terminal 2 — Jalankan action client
```bash
source /opt/ros/humble/setup.bash
python3 action_client.py
```

**Output yang diharapkan (client):**
```
[INFO] [....] [action_client_node]: Goal diterima
[INFO] [....] [action_client_node]: Feedback: 1/10
[INFO] [....] [action_client_node]: Feedback: 2/10
[INFO] [....] [action_client_node]: Feedback: 3/10
...
[INFO] [....] [action_client_node]: Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

**Output yang diharapkan (server):**
```
[INFO] [....] [action_server_node]: Menerima goal order=10
[INFO] [....] [action_server_node]: Mengeksekusi... 1/10
[INFO] [....] [action_server_node]: Mengeksekusi... 2/10
...
[INFO] [....] [action_server_node]: Selesai
```

### Langkah 4: Terminal 3 — Cek daftar action
```bash
source /opt/ros/humble/setup.bash
ros2 action list
```

**Output yang diharapkan:**
```
/fibonacci
```

### Langkah 5: Terminal 3 — Kirim goal dari CLI
```bash
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 5}"
```

**Output yang diharapkan:**
```
Waiting for an action server...
Goal accepted with ID: xxx
Feedback:
    sequence: [0, 1, 1, 2, 3]
Result:
    sequence: [0, 1, 1, 2, 3, 5]
```

**Kesimpulan:** Action adalah komunikasi **goal-feedback-result** — cocok untuk tugas yang butuh waktu lama dan perlu feedback selama proses.

---

## REFERENSI

- [ROS2 Humble: Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- [ROS2 Humble: Writing a simple action server and client (Python)](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)
