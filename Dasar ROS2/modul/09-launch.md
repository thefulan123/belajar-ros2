# MODUL 09: Launch File

**TAG:** otomatisasi / multi-node / konfigurasi

---

## APA ITU LAUNCH FILE?

Launch file adalah file yang menjalankan **banyak node sekaligus** dengan satu perintah.

```bash
# Daripada buka 3 terminal:
ros2 run package node_a  # Terminal 1
ros2 run package node_b  # Terminal 2
ros2 run package node_c  # Terminal 3

# Cukup 1 perintah:
ros2 launch package launch_file.py
```

Launch file ditulis dalam **Python** (ROS2 Humble). File ini mengatur:
- Node apa saja yang dijalankan
- Parameter setiap node
- Namespace (prefix nama node/topic)
- Remapping (mengganti nama topic)

---

## KENAPA ADA?

### Masalah

Robot sungguhan butuh banyak node berjalan bersamaan:
- 1 node sensor
- 2 node motor
- 1 node kamera
- 1 node navigasi
- 1 node odometry

Total **6 terminal** harus dibuka manual. Rentan error:
- Lupa menjalankan node tertentu
- Salah urutan menjalankan node
- Parameter tidak konsisten antar node
- Sulit di-share ke orang lain

### Solusi

Launch file mengotomatiskan semua itu:
```bash
ros2 launch robot_bringup robot.launch.py
```
Satu perintah → semua node jalan dengan parameter yang benar.

---

## CARA KERJA

### Launch File Minimal

```python
# launch/robot.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_belajar',
            executable='talker_node',
            name='talker'
        ),
        Node(
            package='ros2_belajar',
            executable='listener_node',
            name='listener'
        ),
    ])
```

### Parameter di Launch File

```python
Node(
    package='ros2_belajar',
    executable='param_node',
    name='param_node',
    parameters=[{
        'kecepatan': 1.5,
        'nama_robot': 'robot_2',
    }]
)
```

Atau pakai file YAML:
```python
parameters=['config/params.yaml']
```

### Namespace dan Remapping

```python
# Beri namespace agar tidak konflik dengan node lain
Node(
    package='ros2_belajar',
    executable='talker_node',
    name='talker',
    namespace='robot1'  # node jadi /robot1/talker
)

# Remap topic
Node(
    package='ros2_belajar',
    executable='listener_node',
    name='listener',
    remappings=[
        ('/chatter', '/robot1/chatter')  # ganti nama topic
    ]
)
```

### Launch dengan Include

```python
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('robot_bringup'),
                    'launch', 'sensors.launch.py'
                ])
            ])
        ),
    ])
```

---

## CONTOH

### 1. Jalankan 2 node sekaligus
```bash
ros2 launch launch/param_demo.launch.py
```

### 2. Lihat node yang berjalan
```bash
ros2 node list
# Output: /param_node
```

### 3. Jalankan dengan argumen
```python
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('kecepatan', default_value='1.0'),
        Node(
            package='ros2_belajar',
            executable='param_node',
            parameters=[{'kecepatan': LaunchConfiguration('kecepatan')}]
        ),
    ])
```

Jalankan:
```bash
ros2 launch launch/demo.launch.py kecepatan:=2.5
```

---

## COBA INI

**Eksperimen 1 — Launch file sederhana:**
```bash
cd Dasar ROS2/explore/06-launch-params/
source /opt/ros/humble/setup.bash
ros2 launch launch/param_demo.launch.py
```
Node `param_node` berjalan dengan parameter yang sudah diatur di launch file.

**Eksperimen 2 — Buat launch file sendiri:**
Buat file `launch/hello.launch.py`:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtle1'),
        Node(package='turtlesim', executable='turtle_teleop_key', name='teleop1'),
    ])
```
Jalankan: `ros2 launch launch/hello.launch.py`

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `launch file not found` | Path salah | Pastikan file `.launch.py` ada di folder `launch/` |
| `Package 'xxx' not found` | Package belum di-source | `source install/setup.bash` |
| `Executable 'xxx' not found` | Node belum didaftarkan | Tambah ke `entry_points` di `setup.py` |
| `IncludeLaunchDescription error` | File yang di-include tidak ditemukan | Cek path file launch yang di-include |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 08** — Workspace & Package (launch ada di dalam package)
- **Modul 06** — Parameter (launch file sering digunakan untuk set parameter)
- **Praktek: explore/06-launch-params** — contoh launch file dengan parameter

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie jalankan program dengan **upload 1 file `.ino`** ke board. Di ROS2, kita punya **launch file** untuk menjalankan banyak node.

| Aspek | ROS2 Launch | Arduino (upload) |
|-------|-------------|------------------|
| Jumlah program | Banyak node sekaligus | 1 file `.ino` per board |
| Cara jalan | `ros2 launch package file.launch.py` | Upload via USB |
| Argumen | Bisa passing parameter saat launch | Harus edit kode |
| Konfigurasi | Parameter di launch file / YAML | `#define` di kode |
| Multi-board | Satu launch file bisa include launch lain | 1 board = 1 upload |
| Debug | `ros2 node list` — lihat semua node | Serial Monitor — 1 board |

**Intinya:** Launch file = **remote control multi-tasking**. Kamu tekan 1 tombol (1 perintah), semua node jalan dengan setting yang tepat. Arduino = saklar manual — 1 program, 1 board, 1 upload.

---

## 📁 PRAKTIK

Praktik ini menjalankan **launch file** untuk mengotomatiskan multiple node.

### Langkah 1: Buka folder launch
```
cd Dasar ROS2/explore/06-launch-params/
```

### Langkah 2: Lihat isi launch file
Buka file `launch/param_demo.launch.py`:
```python
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
                'nama_robot': 'robot_from_launch',
            }]
        ),
    ])
```

### Langkah 3: Terminal — Jalankan launch file
```bash
source /opt/ros/humble/setup.bash
ros2 launch launch/param_demo.launch.py
```

**Output yang diharapkan:**
```
[INFO] [launch]: All log files can be found in ...
[INFO] [param_node-1]: process started with pid [1234]
[INFO] [....] [param_node]: robot_from_launch: kecepatan 1.5
```

Perhatikan nama robot dan kecepatan berasal dari parameter di launch file — bukan dari nilai default di kode.

### Langkah 4: Terminal 2 — Cek node
```bash
source /opt/ros/humble/setup.bash
ros2 node list
```

**Output yang diharapkan:**
```
/param_node
```

### Langkah 5: Buat launch file sendiri
Buat file `launch/turtlesim.launch.py`:
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtle_sim'),
        Node(package='turtlesim', executable='turtle_teleop_key', name='teleop'),
    ])
```

Jalankan:
```bash
ros2 launch launch/turtlesim.launch.py
```

Satu perintah → turtlesim + teleop jalan bersamaan.

**Kesimpulan:** Launch file menghemat waktu dan mengurangi error dengan menjalankan banyak node sekaligus. Cocok untuk robot yang punya 10+ node yang harus jalan setiap kali.

---

## REFERENSI

- [ROS2 Humble: Launching nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)
- [ROS2 Humble: Creating launch files (Python)](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
- [ROS2 Humble: Using substitutions in launch files](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Using-Substitutions.html)
