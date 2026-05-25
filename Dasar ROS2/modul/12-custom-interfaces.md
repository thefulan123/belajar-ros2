# MODUL 12: Custom Interfaces — .msg / .srv / .action

**TAG:** lanjutan / komunikasi / interfaces

---

## TUJUAN

Setelah modul ini, kamu bisa:
- Memahami kenapa perlu custom interfaces
- Membuat file `.msg` untuk custom topic
- Membuat file `.srv` untuk custom service
- Membuat file `.action` untuk custom action
- Build dan pakai custom interfaces di Python

---

## 1. Kenapa Perlu Custom Interfaces?

ROS2 punya banyak tipe bawaan: `std_msgs/String`, `geometry_msgs/Twist`, dll.
Tapi kadang data kamu **tidak cocok** dengan tipe yang ada.

**Contoh:** Sensor DHT11 kirim suhu (float) + kelembapan (float) + timestamp.
- Bisa pake 3 topic terpisah: `/suhu`, `/kelembapan`, `/timestamp`
- **Lebih baik:** 1 topic dengan custom message `SensorData` yang berisi ketiganya.

**Keuntungan custom interfaces:**
1. **Atomic** — 1 message = 1 kesatuan data yang sinkron
2. **Type-safe** — compiler/type checker tahu strukturnya
3. **Reusable** — bisa dipakai banyak node, bahkan beda bahasa (C++, Python)
4. **Documented** — file `.msg` adalah dokumentasi yang bisa dibaca

---

## 2. Struktur File Interface

Di ROS2, custom interfaces didefinisikan dalam folder di dalam package:

```
my_package/
├── msg/
│   └── SensorData.msg      ← Custom message
├── srv/
│   └── CalculateArea.srv   ← Custom service
├── action/
│   └── NavigateTo.action   ← Custom action
├── CMakeLists.txt
├── package.xml
└── ...
```

Setiap file berisi definisi field dalam format:

```
<type> <nama_field>
<type> <nama_field>
...
```

### Format .msg

```
float32 temperature
float32 humidity
float32 pressure
```

### Format .srv

Dipisahkan dengan `---`:
- **Atas:** request
- **Bawah:** response

```
float32 radius
---
float32 area
string message
```

### Format .action

Dipisahkan dengan `---`:
- **Atas:** goal
- **Tengah:** result
- **Bawah:** feedback

```
float32 target_x
float32 target_y
---
bool success
string status_message
---
float32 current_x  # feedback — posisi terkini
float32 current_y
```

---

## 3. Tipe Data yang Bisa Dipakai

| Kategori | Tipe | Contoh |
|----------|------|--------|
| Primitif | `bool`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`, `float32`, `float64`, `string` | `float32 temperature` |
| Array | Akhiri dengan `[]` | `float32[] temperatures`, `int32[3] rgb` |
| Waktu | `time`, `duration` | `time timestamp`, `duration lifespan` |
| Interface lain | Bisa gunakan tipe dari package lain | `geometry_msgs/Pose pose` |

Array bisa tanpa panjang (`float32[]`) atau fixed-length (`int32[3]`).

---

## 4. Cara Membuat Custom Message (Langkah Demi Langkah)

### Step 1: Buat package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python sensor_msg_pkg
```

### Step 2: Buat folder msg/

```bash
cd sensor_msg_pkg
mkdir msg
```

### Step 3: Buat file `.msg`

Buat `msg/SensorData.msg`:

```
float32 temperature
float32 humidity
float32 pressure
time stamp
```

### Step 4: Edit `package.xml`

Tambahkan dependensi:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

### Step 5: Edit `CMakeLists.txt` (khusus package ament_cmake)

Untuk package Python (`ament_python`), tambahkan di `setup.py`:

```python
from setuptools import setup

package_name = 'sensor_msg_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Register msg files
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nama_kamu',
    maintainer_email='email@example.com',
    description='Custom message package',
    license='Apache 2.0',
)
```

### Step 6: Build

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

### Step 7: Gunakan di Python

```python
from sensor_msg_pkg.msg import SensorData

msg = SensorData()
msg.temperature = 28.5
msg.humidity = 65.0
msg.pressure = 1013.2
```

Cek dengan CLI:

```bash
ros2 interface show sensor_msg_pkg/msg/SensorData
# Output:
# float32 temperature
# float32 humidity
# float32 pressure
# time stamp
```

---

## 5. Cara Membuat Custom Service

### Step 1: Buat file `.srv`

`my_package/srv/CalculateArea.srv`:

```yaml
float32 radius
---
float32 area
string message
```

### Step 2: Build

Sama seperti custom message — colcon build.

### Step 3: Gunakan di Python

**Server:**

```python
from my_package.srv import CalculateArea

def handle_area(req, resp):
    resp.area = 3.14159 * req.radius * req.radius
    resp.message = f"Area = {resp.area:.2f}"
    return resp
```

**Client:**

```python
from my_package.srv import CalculateArea

req = CalculateArea.Request()
req.radius = 5.0

future = cli.call_async(req)
```

---

## 6. Cara Membuat Custom Action

### Step 1: Buat file `.action`

`my_package/action/NavigateTo.action`:

```yaml
float32 target_x
float32 target_y
---
bool success
string status_message
---
float32 current_x
float32 current_y
```

### Step 2: Build

```bash
colcon build
```

### Step 3: Gunakan di Python

**Action server:**

```python
from my_package.action import NavigateTo

def execute_cb(goal_handle):
    for i in range(10):
        feedback = NavigateTo.Feedback()
        feedback.current_x = goal_handle.request.target_x * (i + 1) / 10
        feedback.current_y = goal_handle.request.target_y * (i + 1) / 10
        goal_handle.publish_feedback(feedback)
    goal_handle.succeed()
    return NavigateTo.Result(success=True, status_message="Sampai tujuan")
```

**Action client:**

```python
from my_package.action import NavigateTo

goal = NavigateTo.Goal()
goal.target_x = 5.0
goal.target_y = 3.0

future = cli.send_goal_async(goal)
```

---

## 7. Best Practices

| Praktik Baik | Penjelasan |
|-------------|-----------|
| **Satu file per tipe** | 1 `.msg` = 1 tipe pesan. Jangan gabung-gabung. |
| **Nama deskriptif** | `SensorData.msg`, `MotorCommand.msg` — jelas fungsinya. |
| **Field minimal** | Hanya field yang benar-benar dipakai. |
| **Gunakan timestamp** | Setiap message sensor perlu `time stamp` untuk logging. |
| **Versi field** | Jangan hapus field — tambah yang baru. Breaking change! |
| **Jumlah field wajar** | Max 10-15 field per message. Lebih → pecah jadi beberapa. |

### Contoh Naming Convention

```
SensorData.msg         ← Data sensor gabungan
MotorCommand.msg       ← Perintah motor (kiri+kanan)
RobotStatus.msg        ← Status robot (baterai, mode, error)
DetectionResult.msg    ← Hasil deteksi (objek, confidence, posisi)
Waypoint.msg           ← Titik navigasi (x, y, theta)
```

---

## REFERENSI

- [ROS2 Official: Creating custom msg and srv files](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html)
- [ROS2 Interface concepts](https://docs.ros.org/en/humble/Concepts/Basic/About-Interfaces.html)
- [Available interfaces list](https://github.com/ros2/common_interfaces)
- [.msg specification](https://ros.org/reps/rep-0119.html)

---

## HUBUNGAN DENGAN MODUL LAIN

- **Modul 04 — Topic** (custom message melengkapi std_msgs)
- **Modul 05 — Service** (custom service definition)
- **Modul 07 — Action** (custom action definition)
- **Modul 08 — Workspace & Package** (build process untuk custom interfaces)
- **Praktek: explore/05-custom-msg** — implementasi custom message
- **Penerapan Praktik:** Custom interfaces berguna saat [37-system-integration](../../Penerapan%20ROS2%20pada%20Komponen%20yang%20Umum%20ditemui/explore/37-system-integration/README.md) membutuhkan tipe data gabungan sensor
   Lihat [KORELASI.md](../docs/KORELASI.md) untuk mapping lengkap.

---

## 🔄 ROS2 vs Arduino Biasa

Di Arduino biasa, kita pakai `struct` buat data gabungan:

### Arduino (struct):
```cpp
struct SensorData {
  float temperature;
  float humidity;
  float pressure;
};

SensorData data;
data.temperature = 28.5;
```

### ROS2 (.msg):
```
float32 temperature
float32 humidity
float32 pressure
```

Bedanya: file `.msg` otomatis generate code di **semua bahasa** (C++, Python, dll).
Di Arduino, struct cuma berlaku di 1 sketch itu saja.
