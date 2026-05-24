=== Penerapan ROS2 pada Komponen yang Umum Ditemui ===

Level 2: Praktik menghubungkan komponen elektronik ke ROS2.

Arsitektur dual-track:
  explore/         → 38 komponen, tiap folder standalone micro-ROS + wiring
  referensi/       → Panduan instalasi, daftar komponen, klasifikasi, wiring

Prerequisites:
  - Selesaikan Dasar ROS2/ dulu (modul 01-12)
  - Pahami Node, Topic, Publisher, Subscriber, Callback
  - Instal semua software (lihat referensi/00)

Teknologi:
  - ROS2 Humble
  - micro-ROS (Arduino UNO via Serial, ESP32 via WiFi)
  - Dual board: #if defined(ESP32) || defined(ARDUINO_AVR_UNO)
