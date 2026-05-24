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
