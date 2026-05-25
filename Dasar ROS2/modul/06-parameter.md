# MODUL 06: Parameter

**TAG:** konfigurasi / runtime / fleksibilitas

---

## APA ITU PARAMETER?

Parameter adalah **pengaturan** yang bisa diubah tanpa mengedit kode.

```python
self.declare_parameter('kecepatan', 0.5)   # parameter dengan nilai default
kecepatan = self.get_parameter('kecepatan').value  # baca nilai
```

Parameter memungkinkan kita mengubah perilaku node saat sedang berjalan.

---

## KENAPA ADA?

### Masalah

Tanpa parameter, setiap kali ingin mengubah pengaturan:
```python
# Harus edit kode langsung
KECEPATAN = 0.5  # ← ganti angka ini, save, jalankan ulang
```

Masalah:
- Setiap ganti pengaturan harus restart node
- Tidak praktis kalau node berjalan di robot yang jauh
- Pengaturan keras (hardcoded) — tidak fleksibel

### Solusi

Dengan parameter, pengaturan bisa diubah:
- **Dari command line** saat menjalankan node
- **Dari file konfigurasi** YAML
- **Dari node lain** (via service)
- **Dari CLI** `ros2 param set` saat node berjalan

---

## CARA KERJA

### Mendeklarasikan Parameter

```python
class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')

        # Deklarasi parameter dengan nilai default
        self.declare_parameter('kecepatan', 1.0)
        self.declare_parameter('nama_robot', 'robo_ku')
        self.declare_parameter('aktif', True)

        # Baca parameter
        kecepatan = self.get_parameter('kecepatan').value
        nama = self.get_parameter('nama_robot').value
        aktif = self.get_parameter('aktif').value
```

### Tipe Data Parameter

| Tipe Python | Tipe ROS2 | Contoh |
|-------------|-----------|--------|
| `int` | Integer | `count: 10` |
| `float` | Double | `kecepatan: 0.5` |
| `str` | String | `nama: 'robot_1'` |
| `bool` | Boolean | `aktif: true` |
| `list` | Integer[] / Double[] / String[] | `[1, 2, 3]` |

### Mengubah Parameter dari CLI

```bash
# Lihat semua parameter node
ros2 param list /nama_node

# Lihat nilai parameter
ros2 param get /nama_node kecepatan

# Ubah nilai parameter (langsung, tanpa restart)
ros2 param set /nama_node kecepatan 2.0

# Simpan parameter ke file
ros2 param dump /nama_node

# Load parameter dari file
ros2 param load /nama_node params.yaml
```

### Parameter dari Launch File

```python
# launch/param_demo.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_belajar',
            executable='param_node',
            name='param_node',
            parameters=[{
                'kecepatan': 1.5,
                'nama_robot': 'robot_2',
            }]
        )
    ])
```

### Parameter dari File YAML

```yaml
# params.yaml
param_node:
  ros__parameters:
    kecepatan: 2.0
    nama_robot: 'robot_3'
    aktif: true
```

Muat dari launch file:
```python
parameters=['params.yaml']
```

---

## CONTOH

### Node dengan Parameter

```python
import rclpy
from rclpy.node import Node

class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')

        self.declare_parameter('kecepatan', 1.0)
        self.declare_parameter('nama_robot', 'robo_ku')

        self.timer = self.create_timer(1.0, self.callback)

    def callback(self):
        kecepatan = self.get_parameter('kecepatan').value
        nama = self.get_parameter('nama_robot').value
        self.get_logger().info(f'{nama}: kecepatan {kecepatan}')
```

### Mengubah Parameter Saat Node Berjalan

```bash
# Terminal 1 — jalankan node
python3 param_node.py

# Terminal 2 — ubah parameter saat node berjalan
ros2 param set /param_node kecepatan 2.5
# Node akan langsung pakai kecepatan baru tanpa restart
```

---

## COBA INI

**Eksperimen 1 — Parameter di turtlesim:**
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node

# Di terminal lain
ros2 param list /turtlesim
ros2 param get /turtlesim background_b
ros2 param set /turtlesim background_r 255
ros2 param set /turtlesim background_g 100
ros2 param set /turtlesim background_b 0
ros2 service call /clear turtlesim/srv/Empty
```

**Eksperimen 2 — Simpan dan load parameter:**
```bash
ros2 param dump /turtlesim
# File turtlesim.yaml tersimpan
ros2 param load /turtlesim turtlesim.yaml
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `Invalid parameter name` | Parameter belum dideklarasikan | Panggil `declare_parameter()` dulu |
| `Parameter 'xxx' not set` | Belum di-set dan tidak ada default | Beri default saat `declare_parameter()` |
| `Type mismatch` | Tipe data parameter tidak sesuai | Cek tipe yang benar dengan `ros2 param get` |
| `Permission denied` | Parameter read-only | Beberapa parameter tidak bisa diubah saat runtime |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 05** — Service (parameter menggunakan service internally)
- **Lanjut ke Modul 07** — Action (node sering pakai parameter untuk konfigurasi action)
- **Praktek: explore/06-launch-params** — parameter + launch file
- **Integrasi dengan Modul 09** — Launch (parameter sering di-set dari launch file)
- **Penerapan Praktik:** [37-system-integration](../../Penerapan%20ROS2%20pada%20Komponen%20yang%20Umum%20ditemui/explore/37-system-integration/README.md) — menggunakan parameter untuk threshold suhu/kelembaban
   Lihat [KORELASI.md](../docs/KORELASI.md) untuk mapping lengkap.

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie ganti pengaturan dengan **edit kode → upload ulang**. Di ROS2, pakai **parameter** yang bisa diubah saat runtime.

| Aspek | ROS2 Parameter | Arduino (hardcoded) |
|-------|---------------|--------------------|
| Ubah nilai | `ros2 param set /node nama nilai` | Edit kode → Upload ulang |
| Saat runtime | ✅ Bisa tanpa restart | ❌ Harus upload ulang |
| Default | `declare_parameter('nama', default)` | `#define NAMA value` |
| Tipe aman | Otomatis cek tipe data | Manual — semua terserah programmer |
| File config | YAML — bisa dibaca manusia | N/A |
| Multi-node | Beda parameter tiap node | 1 program = 1 set variable |

**Intinya:** Parameter itu kayak **remote control** — kamu ubah setting tanpa bongkar mesin. Arduino hardcoded itu kayak **setel ulang pabrik** — setiap ganti harus reprogram.

---

## 📁 PRAKTIK

Praktik ini menjalankan node dengan **parameter** dari folder explore.

### Langkah 1: Buka folder explore
```
cd Dasar ROS2/explore/06-launch-params/
```

Folder ini berisi:
- `param_node.py` — node ROS2 dengan parameter
- `launch/param_demo.launch.py` — launch file dengan parameter
- `config/params.yaml` — file konfigurasi YAML

### Langkah 2: Buka `param_node.py`
```python
class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')
        self.declare_parameter('kecepatan', 1.0)
        self.declare_parameter('nama_robot', 'robo_ku')
```

### Langkah 3: Terminal 1 — Jalankan node
```bash
source /opt/ros/humble/setup.bash
python3 param_node.py
```

**Output yang diharapkan:**
```
[INFO] [....] [param_node]: robo_ku: kecepatan 1.0
[INFO] [....] [param_node]: robo_ku: kecepatan 1.0
...
```

### Langkah 4: Terminal 2 — Lihat parameter
```bash
source /opt/ros/humble/setup.bash
ros2 param list /param_node
```

**Output yang diharapkan:**
```
kecepatan
nama_robot
```

### Langkah 5: Terminal 2 — Ubah parameter
```bash
ros2 param set /param_node kecepatan 2.5
```

**Output yang diharapkan:**
```
Set parameter successful
```

Lihat terminal 1 — kecepatan berubah tanpa restart.

### Langkah 6: Jalankan dengan launch file
```bash
source /opt/ros/humble/setup.bash
ros2 launch launch/param_demo.launch.py
```

**Kesimpulan:** Parameter memungkinkan perubahan konfigurasi **tanpa edit kode** dan **tanpa restart node**. Cocok untuk tuning robot (kecepatan, gain PID, dll) saat sedang berjalan.

---

## REFERENSI

- [ROS2 Humble: Understanding parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- [ROS2 Humble: Using parameters in a class (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html)
- [ROS2 Humble: ROS2 YAML parameter format](https://docs.ros.org/en/humble/How-To-Guides/Using-ros2-param-command-line-tools.html)
