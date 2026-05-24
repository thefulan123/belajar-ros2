#!/usr/bin/env python3
"""
smart_garden.py — sistem taman pintar terintegrasi

Node ROS2 yang mengintegrasikan beberapa sensor dan aktuator untuk
otomatisasi taman pintar. Ini adalah CONTOH INTEGRASI — menggabungkan
semua komponen yang sudah dipelajari di explore sebelumnya.

Fitur:
- Siram otomatis jika tanah kering & tidak hujan
- Nyalakan lampu taman jika gelap
- Tampilkan status di LCD

Komponen: Soil Moisture (08), Rain (28), LDR (07), Pump (29), LED (01), LCD (20)

Cara pakai:
  python3 smart_garden.py
"""


# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE — rclpy (ROS2 Python)
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai:
#
# 1. rclpy
#    - Library utama ROS2 Python. WAJIB untuk semua program.
#    - rclpy.init() = inisialisasi, rclpy.spin() = loop utama.
#
# 2. Node (dari rclpy.node)
#    - Kelas dasar node ROS2. Setiap node punya nama unik.
#    - Bisa memiliki publisher, subscriber, timer, service, dll.
#
# 3. Publisher (create_publisher())
#    - Mengirim data ke topic ROS2 secara periodik.
#    - Parameter: tipe_msg, nama_topic, queue_size.
#    - Method: publish(msg) — kirim ke semua subscriber.
#
# 4. Subscription (create_subscription())
#    - Menerima data dari topic ROS2.
#    - Parameter: tipe_msg, nama_topic, callback, qos.
#    - Callback dipanggil otomatis saat ada data masuk.
#
# 5. Timer (create_timer())
#    - Eksekusi fungsi callback secara periodik.
#    - Parameter: interval_detik, callback_function.
#
# 6. Callback
#    - Fungsi yang dipanggil OTOMATIS oleh ROS2.
#    - Bisa dari: timer, subscriber, service, action.
#    - Tidak dipanggil langsung oleh kode kita.
#
# 7. Tipe pesan standar:
#    - std_msgs.msg.Bool     → bool (true/false)
#    - std_msgs.msg.Int32    → int (angka bulat)
#    - std_msgs.msg.Float64  → float (angka desimal)
#    - std_msgs.msg.String   → string (teks)
# ═══════════════════════════════════════════════════════════════

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool, Float64, String

class SmartGarden(Node):
    def __init__(self):
        # super().__init__: inisialisasi node ROS2 dengan nama 'smart_garden'
        super().__init__('smart_garden')

        # ===== PUBLISHERS =====
        # Publisher untuk mengontrol aktuator via topic ROS2
        # Masing-masing topic ini disubscribe oleh node micro-ROS di Arduino

        # pub_pump: kirim perintah ON/OFF ke pompa air (topic /pompa)
        self.pub_pump = self.create_publisher(Bool, 'pompa', 10)
        # pub_led: kirim perintah ON/OFF ke lampu taman (topic /led)
        self.pub_led = self.create_publisher(Bool, 'led', 10)
        # pub_lcd: kirim teks untuk ditampilkan di LCD (topic /lcd)
        self.pub_lcd = self.create_publisher(String, 'lcd', 10)

        # ===== SUBSCRIBERS =====
        # Subscribe ke topic sensor — data dikirim dari node micro-ROS di Arduino

        # create_subscription: daftarkan callback untuk setiap topic sensor
        # Parameter: tipe pesan, nama topic, fungsi callback, queue size
        self.create_subscription(Int32, 'kelembapan_tanah', self.cb_soil, 10)
        self.create_subscription(Bool, 'hujan', self.cb_rain, 10)
        self.create_subscription(Int32, 'cahaya', self.cb_light, 10)
        self.create_subscription(Float64, 'suhu', self.cb_temp, 10)
        self.create_subscription(Float64, 'kelembapan', self.cb_hum, 10)

        # ===== STATE VARIABLES =====
        # Menyimpan nilai sensor terbaru — diupdate oleh callback
        self.soil = 100        # Kelembapan tanah 0-100% (default kering)
        self.is_raining = False  # Status hujan
        self.light = 100       # Intensitas cahaya 0-100% (default terang)
        self.temp = 0.0        # Suhu dalam °C
        self.hum = 0.0         # Kelembapan udara dalam %
        self.pump_on = False   # Status pompa (untuk menghindari perintah berulang)
        self.light_on = False  # Status lampu (untuk menghindari perintah berulang)

        # Timer 2 detik — panggil self.update() secara periodik untuk logika kontrol
        self.timer = self.create_timer(2.0, self.update)
        self.get_logger().info('Smart Garden aktif!')

    # ===== CALLBACK SUBSCRIBER =====
    # Callback ini dipanggil setiap kali ada data baru dari sensor
    # cb_soil: update nilai kelembapan tanah
    def cb_soil(self, msg): self.soil = msg.data
    # cb_rain: update status hujan
    def cb_rain(self, msg): self.is_raining = msg.data
    # cb_light: update intensitas cahaya
    def cb_light(self, msg): self.light = msg.data
    # cb_temp: update suhu
    def cb_temp(self, msg): self.temp = msg.data
    # cb_hum: update kelembapan udara
    def cb_hum(self, msg): self.hum = msg.data

    def update(self):
        """Logika kontrol utama — dipanggil setiap 2 detik oleh timer"""
        # ===== 1. KONTROL POMPA =====
        # Logika: siram jika tanah kering (<30%) dan tidak sedang hujan
        needs_water = self.soil < 30
        if needs_water and not self.is_raining and not self.pump_on:
            # Nyalakan pompa
            self.pump_on = True
            # publish Bool(data=True) ke topic /pompa untuk menyalakan pompa
            self.pub_pump.publish(Bool(data=True))
            self.get_logger().info('Pompa ON (tanah kering)')
        elif (self.soil > 60 or self.is_raining) and self.pump_on:
            # Matikan pompa: tanah sudah basah (>60%) atau hujan
            self.pump_on = False
            self.pub_pump.publish(Bool(data=False))
            self.get_logger().info('Pompa OFF')

        # ===== 2. KONTROL LAMPU TAMAN =====
        # Logika: nyalakan lampu jika gelap (<20%), matikan jika terang (>40%)
        # Ada hysteresis (20/40) untuk mencegah flicker
        if self.light < 20 and not self.light_on:
            self.light_on = True
            self.pub_led.publish(Bool(data=True))
            self.get_logger().info('Lampu taman ON (gelap)')
        elif self.light > 40 and self.light_on:
            self.light_on = False
            self.pub_led.publish(Bool(data=False))
            self.get_logger().info('Lampu taman OFF')

        # ===== 3. UPDATE LCD =====
        # Kirim teks status ke LCD via topic /lcd
        # Format: baris 1 = suhu+kelembapan, baris 2 = kelembapan tanah
        lcd_msg = String()
        lcd_msg.data = f"T:{self.temp:.0f}C H:{self.hum:.0f}%\nTanah:{self.soil}%"
        self.pub_lcd.publish(lcd_msg)

def main():
    # rclpy.init: inisialisasi sistem ROS2
    rclpy.init()
    node = SmartGarden()
    try:
        # rclpy.spin: loop utama — terus berjalan sampai dihentikan
        # Selama spin, semua callback (subscriber + timer) akan diproses
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Tangkap Ctrl+C untuk shutdown yang bersih
        pass
    finally:
        # Bersihkan resource node dan ROS2
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
