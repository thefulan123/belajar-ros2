from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'ros2_basics'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Belajar ROS2',
    maintainer_email='belajar@ros2.local',
    description='Paket ROS2 untuk belajar dasar ROS2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Node dasar
            'talker_node = ros2_basics.talker_node:main',
            'listener_node = ros2_basics.listener_node:main',

            # Service
            'service_server_node = ros2_basics.service_server_node:main',
            'service_client_node = ros2_basics.service_client_node:main',

            # Action
            'action_server_node = ros2_basics.action_server_node:main',
            'action_client_node = ros2_basics.action_client_node:main',

            # Parameter
            'param_node = ros2_basics.param_node:main',

            # Custom message
            'custom_pub_node = ros2_basics.custom_pub_node:main',
            'custom_sub_node = ros2_basics.custom_sub_node:main',
        ],
    },
)
