#!/usr/bin/env python3
# ============================================================
# param_node.py — Node dengan Parameter
#
# Node ini membaca parameter yang bisa diubah
# tanpa perlu edit kode.
#
# Parameter bisa di-set via:
# - Launch file (.launch.py)
# - Command line: ros2 param set
# - YAML config file
#
# Cara jalankan:
#   python3 param_node.py
#   (menggunakan default parameter)
#
#   Atau pakai launch file:
#   ros2 launch launch/param_demo.launch.py
# ============================================================

# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek yang dipakai di file ini:
#
# 1. rclpy
#    - Library utama ROS2 Python. Wajib untuk semua node.
#
# 2. Node
#    - Kelas dasar node ROS2. Setiap node punya nama unik.
#    - Bisa memiliki parameter, publisher, subscriber, timer.
#
# 3. Parameter (declare_parameter() / get_parameter())
#    - Pengaturan node yang bisa diubah tanpa edit kode.
#    - declare_parameter(nama, default) = daftarkan parameter.
#    - get_parameter(nama) = baca nilai parameter saat ini.
#    - Nilai bisa diubah via: launch file, CLI, atau YAML.
#
# 4. rclpy.Parameter (type)
#    - Tipe data parameter ROS2.
#    - Jenis: PARAMETER_STRING, INTEGER, DOUBLE, BOOL, ARRAY.
#    - Digunakan saat SET parameter dari luar.
#
# 5. Timer (create_timer())
#    - Eksekusi callback periodik.
#    - Di sini: baca parameter tiap 2 detik dan log.
# ═══════════════════════════════════════════════════════════════

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.


class ParamNode(Node):
    # (3) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah node yang menggunakan parameter.
    
    Parameter adalah pengaturan yang bisa diubah
    tanpa mengubah kode.
    """

    def __init__(self):
        # (4) Panggil constructor parent dengan nama node UNIK.
        super().__init__('param_node')

        # (5) DEKLARASI PARAMETER — menentukan parameter yang tersedia + nilai default.
        # Sintaks ROS2: self.declare_parameter('nama_param', nilai_default)
        # Parameter bisa diubah dari luar tanpa edit kode:
        #   - Lewat launch file: -p nama_param:=nilai
        #   - CLI: ros2 param set /node_name param_name value
        #   - YAML config file
        # Jika tidak diubah, parameter menggunakan nilai DEFAULT.
        self.declare_parameter('node_name', 'param_node')    # (6) Nama node (string).
        self.declare_parameter('publish_rate', 1.0)          # (7) Interval timer (float, detik).
        self.declare_parameter('message', 'Halo dari param_node!')  # (8) Pesan (string).
        self.declare_parameter('verbose', True)              # (9) Mode verbose (bool).
        self.declare_parameter('max_count', 10)              # (10) Maksimal jumlah pesan (int).

        # (11) MEMBACA NILAI PARAMETER — mengambil nilai dari parameter.
        # Sintaks: self.get_parameter('nama_param').value
        # .value mengembalikan nilai dengan tipe sesuai deklarasi.
        node_name = self.get_parameter('node_name').value
        publish_rate = self.get_parameter('publish_rate').value
        message = self.get_parameter('message').value
        verbose = self.get_parameter('verbose').value
        max_count = self.get_parameter('max_count').value

        # (12) Simpan nilai parameter ke variabel instance.
        self._node_name = node_name
        self._message = message
        self._verbose = verbose
        self._max_count = max_count
        self._count = 0  # (13) Counter internal (bukan parameter).

        # (14) Timer dengan interval dari parameter publish_rate.
        self.timer = self.create_timer(publish_rate, self.timer_callback)

        # (15) Log informasi node jika verbose = True.
        if self._verbose:
            self.get_logger().info(f'Node dimulai: {node_name}')
            self.get_logger().info(f'Publish rate: {publish_rate} detik')
            self.get_logger().info(f'Pesan: {message}')
            self.get_logger().info(f'Maks count: {max_count}')

    def timer_callback(self):
        # (16) CALLBACK TIMER — dipanggil sesuai publish_rate.
        self._count += 1

        # (17) Cetak pesan jika verbose aktif.
        if self._verbose:
            self.get_logger().info(
                f'[{self._count}/{self._max_count}] {self._message}'
            )

        # (18) Berhenti setelah mencapai max_count.
        if self._count >= self._max_count:
            self.get_logger().info('Mencapai max count. Berhenti.')
            self.timer.cancel()  # (19) Hentikan timer.
            rclpy.shutdown()     # (20) Hentikan ROS2.


def main():
    # (21) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    node = ParamNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nNode dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
