import launch
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
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
        Node(
            package='ros2_basics',
            executable='talker_node',
            name='talker',
            output='screen',
        ),
        Node(
            package='ros2_basics',
            executable='listener_node',
            name='listener',
            output='screen',
        ),

        # === SERVICE ===
        Node(
            package='ros2_basics',
            executable='service_server_node',
            name='service_server',
            output='screen',
        ),

        # === ACTION ===
        Node(
            package='ros2_basics',
            executable='action_server_node',
            name='action_server',
            output='screen',
        ),

        # === CUSTOM MSG ===
        Node(
            package='ros2_basics',
            executable='custom_pub_node',
            name='custom_pub',
            output='screen',
        ),
        Node(
            package='ros2_basics',
            executable='custom_sub_node',
            name='custom_sub',
            output='screen',
        ),

        # === PARAMETER ===
        Node(
            package='ros2_basics',
            executable='param_node',
            name='param_demo',
            output='screen',
            parameters=[{
                'publish_rate': 2.0,
                'message': 'Semua node berjalan!',
                'verbose': True,
                'max_count': 5,
            }],
        ),
    ])
