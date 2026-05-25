=== Dasar ROS2 / explore/ ===

Track 1: Standalone Python & Arduino files.

Setiap subfolder adalah proyek INDEPENDEN — bisa dijalankan sendiri
tanpa perlu build system. Cukup: python3 filename.py

Setiap folder explore terkait dengan modul teori di folder modul/.
Baca modul dulu, lalu praktik di explore.

Folder:
   01-minimal-node/     → Node ROS2 paling sederhana      → baca Modul 03 (Node) + Modul 10 (Callback)
   02-pub-sub/          → Publisher + Subscriber (topic)   → baca Modul 04 (Topic)
   03-service/          → Service server + client           → baca Modul 05 (Service)
   04-action/           → Action server + client            → baca Modul 07 (Action)
    05-custom-msg/       → Custom message type               → baca Modul 12 (Custom Interfaces)
   06-launch-params/    → Launch file + parameter           → baca Modul 06 (Parameter) + Modul 09 (Launch)
   07-arduino-uno/      → micro-ROS dengan Arduino UNO      → baca Modul 11 (micro-ROS)

Urutan belajar yang direkomendasikan:
   1. Mulai dari Modul 01-02 (teori environment + CLI)
   2. explore/01-minimal-node + Modul 03 (Node)
   3. explore/02-pub-sub + Modul 04 (Topic)
   4. explore/03-service + Modul 05 (Service)
   5. explore/06-launch-params + Modul 06 (Parameter)
   6. explore/04-action + Modul 07 (Action)
   7. Lanjut ke Modul 08 (Workspace) untuk colcon build
   8. explore/06-launch-params + Modul 09 (Launch)
   9. explore/01-minimal-node + Modul 10 (Callback)
    10. explore/07-arduino-uno + Modul 11 (micro-ROS)
    11. explore/05-custom-msg + Modul 12 (Custom Interfaces)

Cara pakai:
   cd 02-pub-sub/
   python3 talker.py    # terminal 1
   python3 listener.py  # terminal 2
