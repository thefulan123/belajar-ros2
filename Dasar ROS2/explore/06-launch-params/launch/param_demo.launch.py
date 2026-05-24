# ============================================================
# param_demo.launch.py — Launch File dengan Parameter
#
# Launch file adalah cara menjalankan BANYAK node
# sekaligus dengan pengaturan tertentu.
#
# Di sini kita jalankan param_node.py dengan parameter
# yang sudah diatur.
#
# Cara jalankan:
#   ros2 launch launch/param_demo.launch.py
#
# Atau (kalau dari folder explore/06-launch-params/):
#   ros2 launch launch/param_demo.launch.py
# ============================================================

# (1) Import class LaunchDescription — wadah untuk semua action/node.
from launch import LaunchDescription
# (2) Import ExecuteProcess — action untuk menjalankan proses eksternal (misal python3).
from launch.actions import ExecuteProcess


def generate_launch_description():
    # (3) Fungsi WAJIB untuk semua launch file ROS2.
    # ROS2 memanggil fungsi ini untuk mendapatkan daftar node/action.
    """
    Fungsi ini wajib ada. ROS2 memanggilnya untuk
    mendapatkan deskripsi launch.
    """
    return LaunchDescription([
        # (4) LaunchDescription — daftar berisi semua proses yang akan dijalankan.

        # (5) Menjalankan param_node.py dengan parameter kustom.
        # ExecuteProcess — menjalankan perintah di terminal.
        ExecuteProcess(
            cmd=[  # (6) Perintah yang dijalankan (list of strings).
                'python3', 'param_node.py',
                '--ros-args',  # (7) Tanda bahwa argumen berikut adalah ROS2 parameters.
                '-p', 'node_name:=robot_node',    # (8) Parameter: nama node (string).
                '-p', 'publish_rate:=0.5',         # (9) Parameter: interval timer 0.5 detik.
                '-p', 'message:=Robot sedang berjalan...',  # (10) Parameter: pesan.
                '-p', 'verbose:=True',             # (11) Parameter: verbose aktif.
                '-p', 'max_count:=5',              # (12) Parameter: kirim 5 kali lalu berhenti.
            ],
            name='robot_node',  # (13) Nama proses (tampil di terminal).
            output='screen',    # (14) Output langsung ke terminal.
        ),

        # (15) Node KEDUA — menjalankan param_node.py yang SAMA tapi parameter BERBEDA.
        # Ini menunjukkan bahwa satu file bisa digunakan dengan konfigurasi berbeda.
        ExecuteProcess(
            cmd=[
                'python3', 'param_node.py',
                '--ros-args',
                '-p', 'node_name:=sensor_node',    # (16) Nama node berbeda.
                '-p', 'publish_rate:=2.0',          # (17) Interval lebih lambat (2 detik).
                '-p', 'message:=Membaca sensor...', # (18) Pesan berbeda.
                '-p', 'verbose:=True',
                '-p', 'max_count:=3',               # (19) Hanya 3 kali.
            ],
            name='sensor_node',
            output='screen',
        ),
    ])
