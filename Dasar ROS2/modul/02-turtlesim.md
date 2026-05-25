# MODUL 02: ROS2 dengan turtlesim

**TAG:** pengenalan / CLI / visual

---

## APA ITU turtlesim?

turtlesim adalah simulator ROS2 berbentuk kura-kura. Fungsinya:
- Memberikan visualisasi komunikasi ROS2 secara **real-time**
- Bisa dikendalikan dengan perintah keyboard
- Cocok untuk belajar konsep Node, Topic, Service, Action, Parameter

```bash
# Jalankan turtlesim
ros2 run turtlesim turtlesim_node
```

Jendela kura-kura akan muncul — ini adalah **node ROS2** yang berjalan.

---

## KENAPA ADA?

### Masalah

Belajar ROS2 tanpa robot sungguhan itu sulit:
- Tidak bisa lihat efek dari perintah yang diketik
- Konsep abstract (node, topic) sulit dipahami tanpa visual
- Setup robot mahal dan butuh banyak waktu

### Solusi

turtlesim adalah **robot virtual** yang:
- Gratis — langsung tersedia setelah install ROS2
- Visual — kamu bisa lihat kura-kura bergerak
- Interaktif — semua perintah ROS2 bisa dicoba langsung

---

## CARA KERJA

turtlesim terdiri dari dua node utama:

| Node | Fungsi | Cara Jalankan |
|------|--------|---------------|
| `turtlesim_node` | Simulator kura-kura (visual) | `ros2 run turtlesim turtlesim_node` |
| `turtle_teleop_key` | Kontrol keyboard | `ros2 run turtlesim turtle_teleop_key` |

### Komunikasi Antar Node

```
turtle_teleop_key           turtlesim_node
     │                            │
     │  publish /turtle1/cmd_vel  │
     ├──────────────────────────► │
     │   geometry_msgs/Twist      │  Kura-kura bergerak
     │                            │
```

Saat kamu tekan tombol panah:
1. `turtle_teleop_key` mengirim data ke topic `/turtle1/cmd_vel`
2. `turtlesim_node` membaca topic dan menggerakkan kura-kura
3. Kamu lihat efeknya di jendela

### Perintah CLI yang Bisa Dicoba

| Perintah | Fungsi |
|----------|--------|
| `ros2 node list` | Lihat node yang berjalan |
| `ros2 node info /turtlesim` | Info detail node |
| `ros2 topic list` | Lihat topic yang tersedia |
| `ros2 topic echo /turtle1/cmd_vel` | Lihat data yang dikirim |
| `ros2 topic info /turtle1/cmd_vel` | Info topic |
| `ros2 service list` | Lihat service yang tersedia |
| `ros2 action list` | Lihat action yang tersedia |

---

## CONTOH

### 1. Jalankan turtlesim
```bash
# Terminal 1
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```
Jendela biru dengan kura-kura muncul.

### 2. Kendalikan dengan keyboard
```bash
# Terminal 2
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtle_teleop_key
```
Tekan panah atas/bawah/kiri/kanan. Kura-kura bergerak.

### 3. Lihat komunikasi
```bash
# Terminal 3 — lihat topic
source /opt/ros/humble/setup.bash
ros2 topic list
```
Output:
```
/parameter_events
/rosout
/turtle1/cmd_vel
/turtle1/color_sensor
/turtle1/pose
```

### 4. Lihat data yang dikirim teleop
```bash
ros2 topic echo /turtle1/cmd_vel
```
Sambil tekan tombol panah, kamu lihat data velocity (kecepatan) dikirim.

### 5. Panggil service turtlesim
```bash
# Pindahin kura-kura ke posisi (1, 1)
ros2 service call /turtle1/teleport_absolute \
  turtlesim/srv/TeleportAbsolute "{x: 1.0, y: 1.0, theta: 0.0}"

# Ganti background color
ros2 service call /clear turtlesim/srv/Empty
```

### 6. Parameter turtlesim
```bash
# Lihat parameter turtlesim_node
ros2 param list /turtlesim

# Ganti background color
ros2 param set /turtlesim background_r 255
ros2 param set /turtlesim background_g 100
ros2 param set /turtlesim background_b 0
# Panggil /clear untuk apply
ros2 service call /clear turtlesim/srv/Empty
```

---

## COBA INI

**Eksperimen 1 — Spawn kura-kura baru:**
```bash
# Dari CLI, panggil service spawn
ros2 service call /spawn turtlesim/srv/Spawn \
  "{x: 5.0, y: 5.0, theta: 0.0, name: 'kura2_baru'}"
```
Kura-kura baru muncul. Sekarang ada 2 kura-kura!

**Eksperimen 2 — Kirim velocity langsung:**
```bash
# Tanpa teleop, kirim perintah gerak langsung
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 2.0}, angular: {z: 1.0}}" --once
```

**Eksperimen 3 — Reset posisi:**
```bash
ros2 service call /reset turtlesim/srv/Empty
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `package 'turtlesim' not found` | ROS2 belum di-source atau turtlesim belum install | `source /opt/ros/humble/setup.bash` atau `sudo apt install ros-humble-turtlesim` |
| `command not found: ros2` | Belum source | `source /opt/ros/humble/setup.bash` |
| Tidak bisa gerakkan kura-kura | Terminal teleop tidak fokus | Klik di jendela terminal teleop |
| Jendela turtlesim tidak muncul | Display tidak ter-set | `export DISPLAY=:0` (WSL2: install VcXsrv/XLaunch) |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 01** — Environment (sourcing ROS2 diperlukan sebelum menjalankan turtlesim)
- **Lanjut ke Modul 03** — Node (turtlesim_node adalah contoh node ROS2)
- **Modul 04** — Topic (komunikasi teleop → turtlesim via topic)
- **Modul 05** — Service (perintah spawn, reset, teleport adalah service)
- **Modul 07** — Action (belum ada di turtlesim dasar)

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie biasa ngetes kode dengan **LED berkedip** atau **Serial Monitor**. Di ROS2, turtlesim adalah alat tes yang setara.

| Aspek | ROS2 turtlesim | Arduino (LED blink) |
|-------|---------------|---------------------|
| Tujuan | Belajar komunikasi ROS2 | Verifikasi hardware & kode |
| Visual | Kura-kura bergerak di layar | LED nyala/mati |
| Interaksi | Keyboard kontrol | Kode diubah, upload ulang |
| Kompleksitas | Bisa lihat topic, service, action | Cuma 1 program linear |
| Debug | `ros2 topic echo`, `ros2 node list` | Serial.print() |
| Cocok | Belajar ROS2 tanpa robot | Belajar elektronik dasar |

**Intinya:** turtlesim = "Hello World" -nya ROS2. Sederhana, visual, dan langsung ngajarin konsep inti (node, topic, service) tanpa perlu hardware.

---

## 📁 PRAKTIK

Praktik ini menggunakan **turtlesim** untuk memahami komunikasi ROS2 secara visual.

### Langkah 1: Buka terminal 1 — Source & jalankan turtlesim
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```
Jendela biru dengan kura-kura muncul.

### Langkah 2: Terminal 2 — Source & jalankan teleop
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtle_teleop_key
```

### Langkah 3: Gerakkan kura-kura
Tekan tombol **panah atas/bawah/kiri/kanan** di terminal teleop.

### Langkah 4: Terminal 3 — Eksplorasi CLI
```bash
source /opt/ros/humble/setup.bash

# Lihat node
ros2 node list
# Output: /turtlesim

# Lihat topic
ros2 topic list
# Output: /turtle1/cmd_vel, /turtle1/pose, ...

# Lihat data velocity (sambil tekan panah)
ros2 topic echo /turtle1/cmd_vel

# Lihat service
ros2 service list
```

### Langkah 5: Panggil service spawn
```bash
ros2 service call /spawn turtlesim/srv/Spawn \
  "{x: 3.0, y: 3.0, theta: 0.0, name: 'kura2_kedua'}"
```

### Langkah 6: Ganti background
```bash
ros2 param set /turtlesim background_r 50
ros2 param set /turtlesim background_g 150
ros2 param set /turtlesim background_b 200
ros2 service call /clear turtlesim/srv/Empty
```

### Berhenti:
Tekan **Ctrl+C** di semua terminal.

**Kesimpulan:** turtlesim adalah cara paling cepat dan visual untuk memahami bagaimana node, topic, service, dan parameter bekerja di ROS2 — tanpa perlu robot sungguhan.

---

## REFERENSI

- [ROS2 Humble: Understanding nodes with turtlesim](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- [ROS2 Humble: Understanding topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- [ROS2 Humble: Understanding services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- [ROS2 Humble: Understanding parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- [ROS2 Humble: Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
