from setuptools import find_packages, setup  # (1) Setuptools — tools packaging Python.
from glob import glob  # (2) Glob — mencari file dengan pattern (misal *.launch.py).
import os  # (3) OS — path manipulation untuk cross-platform.

package_name = 'ros2_basics'  # (4) Nama package ROS2 — harus sama dengan folder dan package.xml.

setup(
    name=package_name,  # (5) Nama paket.
    version='0.1.0',    # (6) Versi paket.
    # (7) find_packages() — cari semua folder yang berisi __init__.py.
    packages=find_packages(exclude=['test']),
    data_files=[
        # (8) Resource index — ROS2 butuh ini untuk mendeteksi package.
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # (9) package.xml — metadata ROS2 wajib diinstal.
        ('share/' + package_name, ['package.xml']),
        # (10) Launch files — semua file .launch.py akan diinstal.
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],  # (11) Dependencies untuk pip.
    zip_safe=True,  # (12) Izinkan instalasi dalam format zip.
    maintainer='Belajar ROS2',
    maintainer_email='belajar@ros2.local',
    description='Paket ROS2 untuk belajar dasar ROS2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        # (13) ENTRY POINTS — mendaftarkan fungsi main sebagai executable ROS2.
        # Format: 'nama_executable = nama_package.nama_file:fungsi_main'
        # Setelah colcon build, executable ini bisa dipanggil dengan ros2 run.
        'console_scripts': [
            # Node dasar — pub-sub
            'talker_node = ros2_basics.talker_node:main',      # (14) ros2 run ros2_basics talker_node
            'listener_node = ros2_basics.listener_node:main',  # (15) ros2 run ros2_basics listener_node

            # Service
            'service_server_node = ros2_basics.service_server_node:main',  # (16)
            'service_client_node = ros2_basics.service_client_node:main',  # (17)

            # Action
            'action_server_node = ros2_basics.action_server_node:main',  # (18)
            'action_client_node = ros2_basics.action_client_node:main',  # (19)

            # Parameter
            'param_node = ros2_basics.param_node:main',  # (20)

            # Custom message
            'custom_pub_node = ros2_basics.custom_pub_node:main',  # (21)
            'custom_sub_node = ros2_basics.custom_sub_node:main',  # (22)
        ],
    },
)
