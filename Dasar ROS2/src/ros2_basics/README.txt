=== Dasar ROS2 / src/ros2_basics/ ===

Package ROS2 yang berisi semua node untuk Track 2 (colcon).

Fungsi setiap file:
  ros2_basics/
    talker_node.py        → Publisher ke topic /chatter
    listener_node.py      → Subscriber dari /chatter
    service_server_node.py→ Service server (add_two_ints)
    service_client_node.py→ Service client
    action_server_node.py → Action server (fibonacci)
    action_client_node.py → Action client
    param_node.py         → Demo parameter ROS2
    custom_msg_types.py   → Definisi custom message
    custom_pub_node.py    → Publisher custom message
    custom_sub_node.py    → Subscriber custom message

  launch/
    all_nodes.launch.py   → Launch semua node sekaligus

  package.xml             → Dependencies package
  setup.py                → Konfigurasi build Python
