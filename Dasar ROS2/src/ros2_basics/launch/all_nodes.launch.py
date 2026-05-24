import launch  # (1) Library launch ROS2.
from launch import LaunchDescription  # (2) Class LaunchDescription — wadah node.
from launch_ros.actions import Node  # (3) Class Node — untuk menjalankan node ROS2 dari package.


def generate_launch_description():
    # (4) Fungsi WAJIB — ROS2 memanggil ini untuk mendapatkan deskripsi launch.
    """
    Launch file yang menjalankan SEMUA node Dasar ROS2 sekaligus.
    
    Ini menunjukkan integrasi penuh:
    - talker + listener (pub-sub via /chatter)
    - service server + client (via /add_two_ints)
    - action server (siap menerima goal)
    - custom pub + sub (via /sensor_data)
    """
    return LaunchDescription([

        # === PUB-SUB ===
        # (5) Node talker — package: ros2_basics, executable: talker_node.
        Node(
            package='ros2_basics',   # (6) Nama package tempat executable berada.
            executable='talker_node', # (7) Nama executable (dari entry_points di setup.py).
            name='talker',            # (8) Nama node (overrides nama di dalam kode).
            output='screen',          # (9) Output ke terminal (bisa 'log' atau 'screen').
        ),
        # (10) Node listener — subscribe ke /chatter.
        Node(
            package='ros2_basics',
            executable='listener_node',
            name='listener',
            output='screen',
        ),

        # === SERVICE ===
        # (11) Node service server — menyediakan /add_two_ints.
        Node(
            package='ros2_basics',
            executable='service_server_node',
            name='service_server',
            output='screen',
        ),

        # === ACTION ===
        # (12) Node action server — menyediakan /fibonacci.
        Node(
            package='ros2_basics',
            executable='action_server_node',
            name='action_server',
            output='screen',
        ),

        # === CUSTOM MSG ===
        # (13) Node publisher custom message — kirim data sensor.
        Node(
            package='ros2_basics',
            executable='custom_pub_node',
            name='custom_pub',
            output='screen',
        ),
        # (14) Node subscriber custom message — terima data sensor.
        Node(
            package='ros2_basics',
            executable='custom_sub_node',
            name='custom_sub',
            output='screen',
        ),

        # === PARAMETER ===
        # (15) Node dengan parameter — override parameter dari launch file.
        Node(
            package='ros2_basics',
            executable='param_node',
            name='param_demo',
            output='screen',
            parameters=[{  # (16) Parameter di-set via dictionary.
                'publish_rate': 2.0,      # (17) Interval 2 detik.
                'message': 'Semua node berjalan!',  # (18) Pesan kustom.
                'verbose': True,
                'max_count': 5,            # (19) Hanya 5 kali.
            }],
        ),
    ])
