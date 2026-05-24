=== Penerapan ROS2 pada Komponen yang Umum Ditemui / explore/ ===

38+ proyek praktik menghubungkan komponen elektronik ke ROS2 via micro-ROS.

Setiap subfolder berisi:
  *.ino          → Sketch Arduino (micro-ROS) — upload ke board
  *_node.py      → (opsional) Python node untuk PC
  wiring.md      → Tabel koneksi pin + diagram ASCII
  README.md      → Cara jalankan + konsep ROS2

Daftar komponen:
  01-led              → Subscriber Bool, LED ON/OFF
  02-push-button      → Publisher Bool, internal pull-up
  03-buzzer           → Subscriber Int32, frekuensi bunyi
  04-relay            → Subscriber Bool, saklar arus besar
  05-dht-sensor       → Publisher Float64, suhu + kelembapan
  06-potentiometer    → Publisher Int32, 0-100%
  07-ldr              → Publisher Int32, intensitas cahaya
  08-soil-moisture    → Publisher Int32, kelembapan tanah
  09-gas-sensor       → Publisher Int32, gas/asap
  10-flame-sensor     → Publisher Bool, deteksi api
  11-pir-motion       → Publisher Bool, deteksi gerakan
  12-ultrasonic       → Publisher Float64, jarak cm
  13-servo            → Subscriber Int32, sudut 0-180°
  14-motor-dc         → Subscriber Int32+Bool, L298N H-bridge
  15-stepper          → Subscriber Int32, 28BYJ-48
  16-solenoid         → Subscriber Bool, via relay
  17-mpu6050          → 6x Publisher Float64, accel+gyro I2C
  18-vibration        → Subscriber Int32, PWM getaran
  19-load-cell        → Publisher Float64, HX711 + kalibrasi
  20-lcd-i2c          → Subscriber String, LiquidCrystal I2C
  21-oled             → Subscriber String, Adafruit SSD1306
  22-neopixel         → Subscriber String, WS2812B
  23-joystick         → 3x Publisher, X+Y+Bool
  24-rfid             → Publisher String, RC522 SPI
  25-fingerprint      → Publisher Int32, UART
  26-keypad           → Publisher String, 4x4 matrix
  27-water-flow       → Publisher Float64, interrupt counter
  28-rain-sensor      → Publisher Bool, digital
  29-water-pump       → Subscriber Bool, via relay
  30-microphone       → Publisher Int32, peak detection
  31-speaker          → Subscriber Int32, DFPlayer Mini
  32-encoder          → Publisher Int32, rotary encoder
  33-gps              → 4x Publisher, TinyGPSPlus
  34-esp32-wifi       → micro-ROS via WiFi (UDP)
  35-bluetooth        → Bridge HC-05, 2x String
  36-webcam           → PC-side, sensor_msgs/Image (OpenCV)
  37-system-integration→ Arsitektur multi-node
  38-final-project    → Robot monitoring (all-in-one)
