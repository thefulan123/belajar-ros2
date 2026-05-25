# Agent Log — Belajar ROS2 dari Scratch

Setiap perubahan berarti WAJIB dicatat di sini.
Gunakan format di bawah ini.

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Fase 0: Inisialisasi struktur proyek + Git init + konfigurasi

**Files Changed:**
- AGENTS.md — dibuat (aturan agent multi-agent)
- README.md — dibuat (dual language, overview proyek)
- .gitignore — dibuat (Python, ROS2 build, log, dll)
- scripts/source_ros.sh — dibuat (helper source ROS2)
- docs/ERRORS.md — dibuat (panduan error pemula, dual language)
- logs/agent-log.md — dibuat (template + log ini)
- .gitkeep files — dibuat di 12 folder
- Dasar ROS2/Materi.txt — file existing, dipertahankan

**Reason:**
- Proyek baru, perlu struktur yang rapi dan sesuai framework multi-agent.
- Dual-track: explore/ (standalone Python) + src/ (colcon workspace).
- Dual language supaya pembelajar Indonesia bisa belajar istilah Inggris.

**Implementation Details:**
- Struktur dual-track: explore/ (6 subfolder untuk 6 konsep) + src/ (colcon workspace kosong)
- Dual language: Indonesia + Inggris inline per paragraf di README dan docs
- ROS2 Humble terverifikasi: ros2 command OK, rclpy import OK
- Git local config: user.email dan user.name di-set untuk repo ini
- Branch: main

**Result:** success

**Testing:**
- `bash -c 'source /opt/ros/humble/setup.bash && echo $ROS_DISTRO'` → humble
- `python3 -c "import rclpy; print('OK')"` → OK
- `which ros2` → /opt/ros/humble/bin/ros2
- `git status` → clean
- `git log --oneline` → 1 commit

**Next Recommendation:**
- Lanjut ke Fase 1: Node Dasar + Publisher/Subscriber di explore/01-minimal-node/
- Setup GitHub remote (butuh URL repo dari user)

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Restrukturisasi: pindahkan semua konten ke dalam Dasar ROS2/

**Files Changed:**
- README.md — update path references ke Dasar ROS2/
- AGENTS.md — update directory structure
- Dasar ROS2/scripts/source_ros.sh — update LOCAL_WS path
- Dasar ROS2/logs/agent-log.md — tambah entry ini

**Reason:**
- User ingin struktur berlevel: Dasar ROS2, nanti Menengah ROS2, dst.
- Semua file edukasi masuk ke dalam folder level masing-masing.
- Root folder cukup berisi AGENTS.md, README.md, .gitignore.

**Implementation Details:**
- Semua folder (explore/, src/, launch/, config/, scripts/, docs/, logs/, tests/) dipindah ke Dasar ROS2/
- File paths di README, AGENTS.md, dan source_ros.sh diupdate
- Git history tetap terjaga (rename detected)

**Result:** success

**Testing:**
- `git status` — clean
- Struktur diverifikasi via `find .`
- Push ke GitHub sukses

**Next Recommendation:**
- Lanjut ke Fase 1: Node Dasar di Dasar ROS2/explore/01-minimal-node/

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Buat 7 modul pembelajaran + disclaimer + update README

**Files Changed:**
- Dasar ROS2/modul/01-sourcing.md — dibuat
- Dasar ROS2/modul/02-workspace.md — dibuat
- Dasar ROS2/modul/03-package.md — dibuat
- Dasar ROS2/modul/04-create-package.md — dibuat
- Dasar ROS2/modul/05-build-package.md — dibuat
- Dasar ROS2/modul/06-source-workspace.md — dibuat
- Dasar ROS2/modul/07-callback-event-timer.md — dibuat
- Dasar ROS2/docs/disclaimer.md — dibuat
- README.md — tambah daftar modul, update struktur proyek
- AGENTS.md — update struktur direktori

**Reason:**
- User ingin dokumentasi seperti datasheet/modul yang jelaskan WHY bukan cuma WHAT.
- Setiap modul menjawab: kenapa ada, cara kerja, contoh, eksperimen, error umum.

**Implementation Details:**
- Format modul konsisten: APA ITU → KENAPA ADA → CARA KERJA → CONTOH → COBA INI → ERROR UMUM → HUBUNGAN
- Bahasa Indonesia semua (kecuali README root dual language)
- Modul 07 (callback/event/timer) menjadi jembatan ke praktek explore/01

**Result:** success

**Testing:**
- Semua file terbaca dengan benar
- Link dari README ke modul berfungsi (github path URL encoding)

**Next Recommendation:**
- Fase 1: explore/01-minimal-node (node pertama 10 baris)
- Fase 1: explore/02-pub-sub (publisher + subscriber dasar)

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Fase 1: explore/01-minimal-node + explore/02-pub-sub

**Files Changed:**
- Dasar ROS2/explore/01-minimal-node/minimal_node.py — dibuat
- Dasar ROS2/explore/01-minimal-node/run.sh — dibuat
- Dasar ROS2/explore/01-minimal-node/README.md — dibuat
- Dasar ROS2/explore/02-pub-sub/talker.py — dibuat
- Dasar ROS2/explore/02-pub-sub/listener.py — dibuat
- Dasar ROS2/explore/02-pub-sub/run-demo.sh — dibuat
- Dasar ROS2/explore/02-pub-sub/README.md — dibuat
- README.md — update progres Fase 1

**Reason:**
- Praktek pertama: bikin node, paham callback/timer, pub/sub
- Modul 07 (callback/event/timer) langsung diterapkan di sini

**Implementation Details:**
- minimal_node.py: node 10 baris dengan timer callback
- talker.py: publisher ke topic /chatter tiap 1 detik
- listener.py: subscriber dari topic /chatter
- Setiap file bisa di-run langsung dengan python3 (standalone)
- Tidak perlu colcon build

**Result:** success

**Testing:**
- `python3 minimal_node.py` — berhasil, output tiap 1 detik
- `ros2 node list` — menampilkan `minimal_node`
- `ros2 topic list` — menampilkan `/chatter`
- Publisher + subscriber berkomunikasi via topic

**Next Recommendation:**
- Lanjut Fase 2: explore/03-service (service server + client)

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Fase 2: explore/03-service + explore/04-action

**Files Changed:**
- Dasar ROS2/explore/03-service/service_server.py — dibuat
- Dasar ROS2/explore/03-service/service_client.py — dibuat
- Dasar ROS2/explore/03-service/README.md — dibuat
- Dasar ROS2/explore/03-service/run-demo.sh — dibuat
- Dasar ROS2/explore/04-action/action_server.py — dibuat
- Dasar ROS2/explore/04-action/action_client.py — dibuat
- Dasar ROS2/explore/04-action/README.md — dibuat
- Dasar ROS2/explore/04-action/run-demo.sh — dibuat
- README.md — update progres

**Reason:**
- Service: request-response pattern
- Action: goal-feedback-result pattern (tugas panjang)

**Result:** success

**Next Recommendation:**
- Fase 3: explore/05-custom-msg + 06-launch-params

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Fase 3: explore/05-custom-msg + explore/06-launch-params

**Files Changed:**
- explore/05-custom-msg/my_custom_msg.py — dataclass custom message
- explore/05-custom-msg/pub_custom.py — publisher custom msg
- explore/05-custom-msg/sub_custom.py — subscriber custom msg
- explore/05-custom-msg/SensorData.msg — definisi .msg (referensi)
- explore/06-launch-params/param_node.py — node dengan parameter
- explore/06-launch-params/launch/param_demo.launch.py — launch file
- explore/06-launch-params/config/params.yaml — config YAML
- README.md — update progres

**Result:** success

**Next Recommendation:**
- Fase 4: src/ integrasi colcon (workspace package)

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Fase 4: src/ integrasi colcon — package ros2_basics

**Files Changed:**
- Dasar ROS2/src/ros2_basics/ — package ROS2 lengkap
  - package.xml, setup.py, setup.cfg
  - talker_node.py, listener_node.py
  - service_server_node.py, service_client_node.py
  - action_server_node.py, action_client_node.py
  - param_node.py
  - custom_msg_types.py, custom_pub_node.py, custom_sub_node.py
  - launch/all_nodes.launch.py
- README.md — update progres

**Reason:**
- Integrasi penuh semua node dari explore/ ke dalam package colcon
- Bisa dijalankan dengan ros2 launch

**Implementation Details:**
- 11 node dalam satu package ros2_basics
- Launch file menjalankan 7 node sekaligus (talker, listener, service server, action server, custom pub/sub, param)

**Result:** success

**Testing:**
- `colcon build` — berhasil (1 package finished)
- `ros2 pkg list | grep ros2_basics` — package terdeteksi
- `ros2 launch ros2_basics all_nodes.launch.py` — semua 7 node berjalan
- Talker → /chatter → listener ✅
- Custom pub → /sensor_data → custom sub ✅
- Service server + action server siap ✅

**Next Recommendation:**
- Proyek Dasar ROS2 selesai. Lanjut ke Menengah ROS2 kapan saja.

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Arduino UNO + micro-ROS: modul + explore/07

**Files Changed:**
- Dasar ROS2/modul/08-micro-ros-arduino.md — dibuat
- Dasar ROS2/explore/07-arduino-uno/publisher_suhu/publisher_suhu.ino — dibuat
- Dasar ROS2/explore/07-arduino-uno/subscriber_led/subscriber_led.ino — dibuat
- Dasar ROS2/explore/07-arduino-uno/run-agent.sh — dibuat
- Dasar ROS2/explore/07-arduino-uno/README.md — dibuat

**Reason:**
- User ingin belajar ROS2 dengan Arduino UNO
- micro-ROS memungkinkan Arduino berkomunikasi dengan ROS2

**Implementation Details:**
- Modul 08: teori micro-ROS, instalasi, keterbatasan Arduino UNO
- publisher_suhu: kirim data suhu ke /suhu tiap 2 detik
- subscriber_led: terima perintah boolean untuk LED dari /led
- run-agent.sh: script untuk jalankan micro-ROS agent

**Result:** success

**Testing:**
- Tidak bisa diuji tanpa hardware Arduino
- Kode diverifikasi secara logika (mirip contoh resmi micro-ROS)

**Next Recommendation:**
- Jika Arduino tersedia, ikuti panduan instalasi di modul 08
- Setelah itu upload sketch dan coba komunikasi ROS2

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Tambah 4 modul inti ROS2 (node, topic, service, action)

**Files Changed:**
- Dasar ROS2/modul/09-node.md — dibuat (konsep node ROS2)
- Dasar ROS2/modul/10-topic-pub-sub.md — dibuat (topic, publisher, subscriber)
- Dasar ROS2/modul/11-service.md — dibuat (request-response)
- Dasar ROS2/modul/12-action.md — dibuat (goal-feedback-result)
- Dasar ROS2/Materi.txt — update, mapping ke modul
- README.md — update daftar modul
- AGENTS.md — update struktur

**Reason:**
- User noticed modul/ tidak punya modul untuk konsep inti ROS2
- Sekarang semua 6 konsep dari Materi.txt punya modul masing-masing

**Result:** success

**Testing:**
- Modul 09-12 dibaca, format konsisten dengan modul sebelumnya
- Materi.txt sekarang mapping: node→09, topic→10, publisher→10, subscriber→10, service→11, action→12

**Next Recommendation:**
- Semua modul (01-12) + explore (01-07) + integrasi workspace selesai.
- Lanjut ke Menengah ROS2 kapan saja.

---

## [2026-05-25]

**Agent:** opencode

**Task:**
- Tambah komentar edukasi Bahasa Indonesia baris-per-baris ke semua file Python/Arduino (27 file)

**Files Changed:**
- `Dasar ROS2/explore/01-minimal-node/minimal_node.py` — komentar edukasi
- `Dasar ROS2/explore/02-pub-sub/talker.py` — komentar edukasi
- `Dasar ROS2/explore/02-pub-sub/listener.py` — komentar edukasi
- `Dasar ROS2/explore/03-service/service_server.py` — komentar edukasi
- `Dasar ROS2/explore/03-service/service_client.py` — komentar edukasi
- `Dasar ROS2/explore/04-action/action_server.py` — komentar edukasi
- `Dasar ROS2/explore/04-action/action_client.py` — komentar edukasi
- `Dasar ROS2/explore/05-custom-msg/my_custom_msg.py` — komentar edukasi
- `Dasar ROS2/explore/05-custom-msg/pub_custom.py` — komentar edukasi
- `Dasar ROS2/explore/05-custom-msg/sub_custom.py` — komentar edukasi
- `Dasar ROS2/explore/06-launch-params/param_node.py` — komentar edukasi
- `Dasar ROS2/explore/06-launch-params/launch/param_demo.launch.py` — komentar edukasi
- `Dasar ROS2/explore/07-arduino-uno/publisher_suhu/publisher_suhu.ino` — komentar edukasi
- `Dasar ROS2/explore/07-arduino-uno/subscriber_led/subscriber_led.ino` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/talker_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/listener_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/service_server_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/service_client_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/action_server_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/action_client_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/param_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/custom_msg_types.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/custom_pub_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/ros2_basics/custom_sub_node.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/launch/all_nodes.launch.py` — komentar edukasi
- `Dasar ROS2/src/ros2_basics/setup.py` — komentar edukasi

**Reason:**
- Semua file Python/Arduino perlu komentar edukasi Bahasa Indonesia baris-per-baris
- Membantu pemula memahami API, sintaks, dan konsep ROS2
- Setiap fungsi ROS2 utama diberi penjelasan: APA, MENGAPA, dan SINTAKS

**Implementation Details:**
- Format: `kode  # (nomor) Penjelasan Bahasa Indonesia`
- Fungsi ROS2 yang dijelaskan: rclpy.init(), Node(), create_publisher(), create_subscription(), create_service(), create_client(), rclpy.spin(), get_logger(), declare_parameter(), rclpy.shutdown()
- Komentar mencakup: (a) APA fungsi, (b) MENGAPA perlu, (c) SINTAKS ROS2
- Arduino .ino files: penjelasan rclc_* functions dalam Bahasa Indonesia
- Launch file & setup.py: penjelasan struktur packaging ROS2
- Kode program TIDAK diubah, hanya ditambahi komentar

**Result:** success

**Testing:**
- Semua file diverifikasi: kode asli tidak berubah, hanya komentar ditambah
- Total: 27 file berhasil diedit

**Next Recommendation:**
- Lanjut ke Menengah ROS2 kapan saja.

---

## 2026-05-25 — Revisi Modul: Tambah Bagian PRAKTIK Step-by-Step

**Agent:** big-pickle (main)

**Task Description:**
Setiap modul (01-12) ditambahi bagian "📁 PRAKTIK" di akhir file yang berisi:
1. Direktori folder yang harus dibuka (full path)
2. Langkah-langkah terminal step-by-step (buka terminal → cd → source → run)
3. Output yang diharapkan di setiap langkah

**Files Changed:**
- `Dasar ROS2/modul/01-sourcing.md` — Praktik: source setup.bash + verifikasi PATH & ros2
- `Dasar ROS2/modul/02-workspace.md` — Praktik: buat workspace ~/ros2_ws/src
- `Dasar ROS2/modul/03-package.md` — Praktik: ros2 pkg list + eksplorasi package
- `Dasar ROS2/modul/04-create-package.md` — Praktik: ros2 pkg create package_belajar
- `Dasar ROS2/modul/05-build-package.md` — Praktik: colcon build + cek folder hasil
- `Dasar ROS2/modul/06-source-workspace.md` — Praktik: source install/setup.bash + verifikasi
- `Dasar ROS2/modul/07-callback-event-timer.md` — Praktik: jalankan explore/01-minimal-node/minimal_node.py
- `Dasar ROS2/modul/08-micro-ros-arduino.md` — Praktik: upload & jalankan explore/07-arduino-uno/
- `Dasar ROS2/modul/09-node.md` — Praktik: jalankan node + ros2 node list
- `Dasar ROS2/modul/10-topic-pub-sub.md` — Praktik: talker + listener + ros2 topic echo
- `Dasar ROS2/modul/11-service.md` — Praktik: service_server + service_client + ros2 service call
- `Dasar ROS2/modul/12-action.md` — Praktik: action_server + action_client + ros2 action send_goal

**Reason:**
Pembelajar pemula perlu panduan langkah-demi-langkah yang eksplisit — folder mana dibuka, terminal apa diketik, output apa yang diharapkan. Sebelumnya modul hanya berisi teori dan eksperimen umum tanpa panduan praktik terstruktur.

**Implementation Details:**
- Setiap modul mendapat bagian "📁 PRAKTIK" setelah "HUBUNGAN DENGAN MODUL LAIN"
- Modul 01-06 link ke praktik terminal (sourcing, workspace, package, build)
- Modul 07-12 link ke folder `explore/` dengan full path `/mnt/e/Learn ROS2 from Scratch/Dasar ROS2/explore/`
- Setiap langkah berisi: perintah bash + output yang diharapkan
- Jika butuh 2+ terminal, ditulis eksplisit "Terminal 1", "Terminal 2", dst
- Bahasa Indonesia, format konsisten

**Result:** success

**Testing:**
- 12 file diverifikasi: bagian PRAKTIK muncul di akhir setiap modul
- Output contoh diverifikasi cocok dengan kode di explore/ dan ekspektasi ROS2

**Next Recommendation:**
- Buat video/screenshot untuk setiap langkah praktik
- Tambah modul 13 tentang tf2 (transformasi koordinat)

---

## 2026-05-25 — Setup LSP (Pyright) untuk ROS2 Python

**Agent:** big-pickle (main)

**Task Description:**
Setup Language Server Protocol (LSP) agar AI agent bisa mendeteksi error/diagnostic Python ROS2 secara otomatis.

**Files Changed:**
- `opencode.json` (baru) — enable LSP + konfigurasi pyright-langserver
- `pyrightconfig.json` (baru) — extraPaths ke ROS2 Python packages

**Reason:**
Tanpa LSP, agent tidak bisa mendeteksi error import, type mismatch, dll. Dengan LSP, agent mendapat diagnostic real-time dari pyright.

**Implementation Details:**
- Install `pyright` via `npm install -g pyright` (v1.1.409)
- opencode.json: konfigurasi LSP server dengan full path binary `/home/soke/.npm-global/bin/pyright-langserver`
- pyrightconfig.json: extraPaths menunjuk ke `/opt/ros/humble/local/lib/python3.10/dist-packages/` (lokasi rclpy, std_msgs, dll)
- Verifikasi: pyright report 0 error pada semua file explore/

**Result:** success

**Testing:**
- `pyright Dasar\ ROS2/explore/02-pub-sub/talker.py` → 0 errors (sebelumnya 3 errors unresolved import)
- `pyright Dasar\ ROS2/explore/03-service/service_server.py` → 0 errors
- `pyright Dasar\ ROS2/explore/04-action/action_server.py` → 0 errors
- `pyright Dasar\ ROS2/explore/01-minimal-node/minimal_node.py` → 0 errors

**Next Recommendation:**
- Restart opencode agar konfigurasi LSP aktif
- Jika ada error LSP, cek `pyright --version` dan pastikan pyright di PATH

---

## 2026-05-25 — DOCX Update + PENJELASAN DATA STRUCTURE

**Agent:** big-pickle (main)

**Task Description:**
1. Update file .docx di `Dasar ROS2/modul/` agar punya bagian PRAKTIK (sama seperti .md)
2. Tambah "PENJELASAN DATA STRUCTURE" ke semua file .py dan .ino yang belum punya

**Files Changed (DOCX):**
- 12 file .docx di `Dasar ROS2/modul/` — ditambahi PRAKTIK section (via python-docx)

**Files Changed (PENJELASAN DATA STRUCTURE — Dasar ROS2):**
- `explore/01-minimal-node/minimal_node.py` — PENJELASAN: rclpy, Node, Timer, Callback, spin()
- `explore/02-pub-sub/talker.py` — PENJELASAN: rclpy, Node, Publisher, String, Timer
- `explore/02-pub-sub/listener.py` — PENJELASAN: rclpy, Node, Subscription, Callback, String
- `explore/03-service/service_server.py` — PENJELASAN: rclpy, Node, Service Server, AddTwoInts
- `explore/03-service/service_client.py` — PENJELASAN: rclpy, Node, Client, Future, Timer polling
- `explore/04-action/action_server.py` — PENJELASAN: rclpy, Node, ActionServer, Fibonacci, async
- `explore/04-action/action_client.py` — PENJELASAN: rclpy, Node, ActionClient, Feedback, Future
- `explore/05-custom-msg/my_custom_msg.py` — PENJELASAN: dataclass, custom msg concept, .msg files
- `explore/05-custom-msg/pub_custom.py` — PENJELASAN: rclpy, Publisher, JSON, SensorData
- `explore/05-custom-msg/sub_custom.py` — PENJELASAN: rclpy, Subscription, JSON, SensorData
- `explore/06-launch-params/param_node.py` — PENJELASAN: rclpy, Node, Parameter, declare_parameter
- `explore/06-launch-params/launch/param_demo.launch.py` — PENJELASAN: LaunchDescription, ExecuteProcess
- `explore/07-arduino-uno/publisher_suhu/publisher_suhu.ino` — PENJELASAN: micro-ROS C structures
- `explore/07-arduino-uno/subscriber_led/subscriber_led.ino` — PENJELASAN: micro-ROS C structures

**Files Changed (PENJELASAN DATA STRUCTURE — Penerapan ROS2):**
- 36 file .ino — semua sketch Arduino diberi PENJELASAN micro-ROS (rcl_node_t, rcl_publisher_t, rcl_subscription_t, rclc_executor_t, rclc_support_t, rcl_allocator_t, rcl_timer_t, std_msgs types)
- 21 file .py — semua Python node diberi PENJELASAN rclpy (rclpy, Node, Publisher, Subscription, Timer, Callback, tipe pesan standar)

**Reason:**
Pembelajar perlu memahami data structure apa saja yang dipakai di setiap file dan fungsinya masing-masing. DOCX perlu konsisten dengan MD.

**Implementation Details:**
- DOCX: Python script dengan python-docx, parse PRAKTIK dari .md lalu insert ke .docx sebagai formatted paragraphs
- .ino: PENJELASAN ditambahkan setelah header comment `/* */`, sebelum #include
- .py: PENJELASAN ditambahkan setelah docstring/banner, sebelum import
- Script Python untuk batch processing 57 file Penerapan ROS2

**Result:** success

**Testing:**
- 12 file .docx diverifikasi: PRAKTIK section muncul di akhir
- 71 file code diverifikasi: PENJELASAN DATA STRUCTURE muncul di setiap .py dan .ino
- Semua file yang sudah punya PENJELASAN sebelumnya tidak di-double

**Next Recommendation:**
- Cek konsistensi penjelasan di Penerapan ROS2/referensi/ files
- Buat modul ringkasan data structure ROS2

---

## 2026-05-25 — Perbandingan ROS2 vs Arduino Biasa (Dasar + Penerapan)

**Agent:** big-pickle (main)

**Task Description:**
Tambah tabel perbandingan "ROS2 vs Arduino Biasa" di tiap modul pembelajaran dan tiap README komponen — menjelaskan apa bedanya kalau anak robotik newbie cuma praktek tanpa ROS2 (pake Arduino IDE aja).

**Files Changed:**
- 12 modul `Dasar ROS2/modul/` — tabel perbandingan per konsep (sourcing, workspace, package, build, callback, node, topic, service, action, dsb)
- 38 README `Penerapan ROS2/explore/*/README.md` — perbandingan spesifik per komponen (LED, button, servo, dht, ultrasonic, dsb)

**Reason:**
Pembelajar newbie sering bertanya: "Kenapa harus ribet pake ROS2? Arduino aja cukup." Bagian ini menjawab langsung dengan perbandingan konkret — kode Arduino vs kode ROS2, table perbedaan, dan kapan pake yang mana.

**Implementation Details:**
- Dasar modul: tiap modul dapet section sebelum PRAKTIK, fokus perbedaan KONSEP (callback vs delay, topic vs serial, service vs manual protocol, action vs state machine)
- Penerapan: tiap README dapet section setelah konten existing, fokus perbedaan per KOMPONEN (subscriber vs digitalWrite, publisher vs analogRead)
- Template publisher: "Sensor → publish → seluruh sistem ROS2 vs Serial Monitor doang"
- Template subscriber: "Dikontrol dari mana aja via topic vs fixed di sketch"
- Kategorisasi otomatis berdasarkan kode aktual (bukan komentar)
- Special handling untuk 36-webcam (OpenCV vs sensor_msgs) dan 37-system-integration (multi-node vs 1 sketch)

**Result:** success

**Testing:**
- 12 modul diverifikasi: perbandingan muncul sebelum PRAKTIK
- 38 README diverifikasi: 23 publisher template, 13 subscriber template, 2 special
- Publisher files: button, sensor, joystick, gps, dll → template sensor
- Subscriber files: led, servo, motor, lcd, dll → template aktuator
- Webcam → OpenCV comparison
- System integration → multi-node comparison

**Next Recommendation:**
- Review referensi/ folder di Penerapan ROS2
- Tambah modul praktikum untuk final project

---

## 2026-05-25 — Re-align modul order with ROS2 Humble docs + fix portability

**Agent:** big-pickle (main)

**Task Description:**
1. Fix hardcoded machine-specific paths (portability)
2. Re-align all modul order + naming to match official ROS2 Humble Beginner tutorials
3. Consolidate workspace/package/build/source modules
4. Add 3 new modules (turtlesim, parameter, launch)

**Files Changed (24 files):**

| Change | Files |
|--------|-------|
| **Portability fix** | `opencode.json`, `Dasar ROS2/scripts/source_ros.sh` |
| **Portability fix (paths)** | `07-callback-event-timer.md` (now `10-callback-timer.md`), `08-micro-ros-arduino.md` (now `11-micro-ros.md`), `09-node.md` (now `03-node.md`), `10-topic-pub-sub.md` (now `04-topic-pub-sub.md`), `11-service.md` (now `05-service.md`), `12-action.md` (now `07-action.md`) |
| **Git mv rename (7)** | `01-sourcing→01-environment`, `09-node→03-node`, `10-topic-pub-sub→04-topic-pub-sub`, `11-service→05-service`, `12-action→07-action`, `07-callback-event-timer→10-callback-timer`, `08-micro-ros-arduino→11-micro-ros` |
| **Git rm delete (5)** | `02-workspace`, `03-package`, `04-create-package`, `05-build-package`, `06-source-workspace` (merged into 08) |
| **Create new (4)** | `02-turtlesim.md`, `06-parameter.md`, `08-workspace-package.md`, `09-launch.md` |
| **Update references** | `README.md`, `Materi.txt`, `modul/README.txt`, `explore/01-minimal-node/README.md`, `explore/02-pub-sub/README.md`, `explore/07-arduino-uno/README.md` |

**Reason:**
- Hardcoded `/home/soke/` and `/mnt/e/` paths made repo non-portable for anyone cloning
- Learning order didn't match official ROS2 Humble docs (https://docs.ros.org/en/humble/)
- Workspace/package/build/source were 5 separate files but conceptually 1 workflow
- Missing modules for turtlesim (CLI intro), parameters, and launch files

**Implementation Details:**
- New order: Environment → turtlesim → Node → Topic → Service → Parameter → Action → Workspace-Package → Launch → Callback-Timer → micro-ROS
- Consolidated `08-workspace-package.md` covers: workspace structure, package anatomy, `ros2 pkg create`, `colcon build`, sourcing workspace — one end-to-end workflow
- Each renamed file updated: MODUL number, HUBUNGAN DENGAN MODUL LAIN cross-refs, added REFERENSI section linking to official docs
- REFERENSI added to all 11 modules (new + renamed) — links to docs.ros.org
- Portability: `opencode.json` uses bare `pyright-langserver` command; `source_ros.sh` uses `$(dirname "$(realpath "$0")")/../src` instead of hardcoded path

**Result:** success

**Testing:**
- `git status` → 24 files staged, 4 untracked created, 5 deleted, 7 renamed
- `git log --oneline -1` → commit `47c7e7c`
- `git push` → successful to origin/main
- Cross-references verified: all explore READMEs point to correct new modul numbers
- Modul files checked: titles, HUBUNGAN sections, and REFERENSI all use new numbering

**Next Recommendation:**
- Add explore/README.txt with modul-explore mapping
- Create docx versions from updated .md files (if needed)
- Consider adding 2 more modules: Custom Interfaces (explore/05) and ROS2 Tools (ros2doctor, ros2bag)

---

## 2026-05-25 — Fix cross-reference gaps + update explore/README.txt

**Agent:** big-pickle (main)

**Task Description:**
1. Run consistency audit on all 11 modul files
2. Fix 2 missing forward references (Modul 07 → 08, Modul 10 → 11)
3. Add Modul 06 reference to Modul 02 (parameter in turtlesim)
4. Update explore/README.txt with modul-explore mapping

**Files Changed:**
- `Dasar ROS2/modul/02-turtlesim.md` — add Modul 06 (Parameter) reference
- `Dasar ROS2/modul/07-action.md` — add "Lanjut ke Modul 08"
- `Dasar ROS2/modul/10-callback-timer.md` — add "Lanjut ke Modul 11"
- `Dasar ROS2/explore/README.txt` — add modul mapping table + recommended learning order

**Reason:**
- Consistency audit revealed minor gaps: 07 didn't point forward to 08, 10 didn't point to 11
- turtlesim uses `ros2 param` commands but didn't reference the Parameter module
- explore/README.txt lacked modul references for learners

**Result:** success

**Testing:**
- `git commit f95f042` — pushed to main
- All 11 modul cross-references now form a complete chain (01→02→03→04→05→06→07→08→09→10→11)

**Next Recommendation:**
- Re-generate .docx files from new .md structure
- Consider adding Custom Interfaces module (matching explore/05-custom-msg)

---

## 2026-05-25 — Fix type hints in explore code + pyright 0 errors

**Agent:** big-pickle (main)

**Task Description:**
Review all 14 code files in explore/ and fix any issues found.

**Files Changed:**
- `Dasar ROS2/explore/05-custom-msg/my_custom_msg.py` — `List[int]` → `Optional[List[int]]` for error_codes
- `Dasar ROS2/explore/06-launch-params/param_node.py` — add None guards for publish_rate, max_count
- `Dasar ROS2/explore/03-service/service_client.py` — add type: ignore for rclpy dynamic type
- `Dasar ROS2/explore/04-action/action_client.py` — add type: ignore for rclpy dynamic type

**Reason:**
- Review request from user: ensure all explore code is clean and consistent
- pyright was reporting 4 type errors (1 genuine, 3 rclpy stub limitations)

**Result:** success

**Testing:**
- `npx pyright Dasar ROS2/explore/` → **0 errors, 0 warnings, 0 informations**
- All 14 code files (.py + .ino) have: shebang, banner, PENJELASAN DATA STRUCTURE, docstrings, inline comments, KeyboardInterrupt handling, proper cleanup

**Next Recommendation:**
- Re-generate .docx files from new .md structure
- Consider adding Custom Interfaces module (matching explore/05-custom-msg)
