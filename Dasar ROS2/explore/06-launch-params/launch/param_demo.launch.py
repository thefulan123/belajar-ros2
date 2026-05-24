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

from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():
    """
    Fungsi ini wajib ada. ROS2 memanggilnya untuk
    mendapatkan deskripsi launch.
    """
    return LaunchDescription([

        # Jalankan param_node.py dengan parameter kustom
        ExecuteProcess(
            cmd=[
                'python3', 'param_node.py',
                '--ros-args',
                '-p', 'node_name:=robot_node',
                '-p', 'publish_rate:=0.5',
                '-p', 'message:=Robot sedang berjalan...',
                '-p', 'verbose:=True',
                '-p', 'max_count:=5',
            ],
            name='robot_node',
            output='screen',
        ),

        # Node kedua dengan parameter berbeda
        ExecuteProcess(
            cmd=[
                'python3', 'param_node.py',
                '--ros-args',
                '-p', 'node_name:=sensor_node',
                '-p', 'publish_rate:=2.0',
                '-p', 'message:=Membaca sensor...',
                '-p', 'verbose:=True',
                '-p', 'max_count:=3',
            ],
            name='sensor_node',
            output='screen',
        ),
    ])
