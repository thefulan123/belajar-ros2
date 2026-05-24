# explore/27-water-flow — Baca Debit Air via ROS2

## Tujuan

Belajar **Publisher dengan interrupt counter** — menghitung pulse flow sensor dan kirim debit air.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/debit_air` |
| Tipe | `std_msgs/Float64` |
| Data | Debit air dalam L/min |
| Topic | `/volume_air` |
| Tipe | `std_msgs/Float64` |
| Data | Total volume dalam Liter |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `water_flow.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /debit_air
# data: 0.0 → tidak ada aliran
# data: 2.5 → 2.5 L/menit

ros2 topic echo /volume_air
# data: 5.3 → total 5.3 Liter
```

## Coba Ini

1. **Tiup sensor** — putaran kincir menghasilkan pulse (kalau berani)
2. **Alirkan air dari selang** — ukur debit wastafel Anda
3. **Integrasi relay (explore/04):** Matikan pompa jika volume > threshold
4. **Integrasi LCD (explore/20):** Tampilkan total volume pemakaian air
