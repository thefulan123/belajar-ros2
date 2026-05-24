# Belajar ROS2 dari Scratch — Learn ROS2 from Scratch

**ID:** Proyek ini adalah panduan belajar ROS2 untuk pemula. Setiap konsep dijelaskan satu per satu dengan kode yang bisa langsung dijalankan.

**EN:** This is a beginner-friendly ROS2 learning guide. Each concept is explained step by step with runnable code.

---

## Daftar Isi / Table of Contents

- [Tujuan / Purpose](#tujuan--purpose)
- [Cara Belajar / How to Learn](#cara-belajar--how-to-learn)
- [Struktur Proyek / Project Structure](#struktur-proyek--project-structure)
- [Persyaratan / Requirements](#persyaratan--requirements)
- [Instalasi / Installation](#instalasi--installation)
- [Cara Menjalankan / How to Run](#cara-menjalankan--how-to-run)
- [ROS2 Graph Overview](#ros2-graph-overview)
- [Tips Debugging / Debugging Tips](#tips-debugging--debugging-tips)
- [Catatan Belajar / Learning Notes](#catatan-belajar--learning-notes)
- [Progres / Progress](#progres--progress)
- [Lisensi / License](#lisensi--license)

---

## Tujuan / Purpose

**ID:**
Repo ini dibuat untuk belajar ROS2 dari **benar-benar nol**. Targetnya:
- Paham konsep Node, Topic, Publisher, Subscriber, Service, Action
- Bisa bikin node sendiri
- Bisa menghubungkan beberapa node
- Siap lanjut ke robot sungguhan

**EN:**
This repo is built to learn ROS2 from **absolute zero**. Goals:
- Understand Node, Topic, Publisher, Subscriber, Service, Action
- Be able to create your own nodes
- Be able to connect multiple nodes
- Ready to move to real robots

---

## Cara Belajar / How to Learn

**ID:** Proyek ini punya **level** yang naik bertahap. Setiap level isinya:

| Level | Folder | Isi |
|-------|--------|-----|
| **Dasar ROS2** | `Dasar ROS2/` | Node, Topic, Publisher, Subscriber, Service, Action |
| **Menengah ROS2** | `Menengah ROS2/` | (akan datang) |

Setiap level punya **2 jalur belajar (dual-track)**:

| Track | Folder | Cara Pakai | Untuk Apa? |
|-------|--------|------------|------------|
| **Track 1 — Explore** | `Dasar ROS2/explore/` | `python3 file.py` | Belajar 1 konsep, langsung lihat hasil |
| **Track 2 — Workspace** | `Dasar ROS2/src/` | `colcon build + ros2 run` | Integrasi semua node jadi satu sistem |

Kenapa 2 track? Biar kamu bisa **fokus belajar konsep dulu** tanpa pusing soal build system. Setelah paham, baru masuk ke cara "beneran" ROS2.

**EN:** This project has **levels** that increase step by step:

| Level | Folder | Content |
|-------|--------|---------|
| **Basic ROS2** | `Dasar ROS2/` | Node, Topic, Publisher, Subscriber, Service, Action |
| **Intermediate ROS2** | `Menengah ROS2/` | (coming soon) |

Each level has **2 learning tracks**:

| Track | Folder | Usage | Purpose |
|-------|--------|-------|---------|
| **Track 1 — Explore** | `Dasar ROS2/explore/` | `python3 file.py` | Learn 1 concept, see results immediately |
| **Track 2 — Workspace** | `Dasar ROS2/src/` | `colcon build + ros2 run` | Integrate all nodes into one system |

Why 2 tracks? So you can **focus on learning concepts first** without worrying about the build system. Once understood, move to the "real" ROS2 workflow.

**Alur belajar / Learning flow:**

```
Fase 0: Inisialisasi proyek ✅ (kamu di sini / you are here)
Fase 1: Node Dasar + Publisher/Subscriber
Fase 2: Service & Client
Fase 3: Action
Fase 4: Custom Interface (.msg / .srv)
Fase 5: Launch File & Parameter
Fase 6: Integrasi penuh di workspace
```

---

## Struktur Proyek / Project Structure

```
Learn ROS2 from Scratch/
│
├── AGENTS.md              # AI agent rules
├── README.md              # File ini / This file
├── .gitignore
│
├── Dasar ROS2/            # LEVEL 1: Basic ROS2
│   ├── Materi.txt         #   Daftar topik
│   ├── explore/           #   TRACK 1: Standalone Python files
│   │   ├── 01-minimal-node/   # Run: python3 filename.py
│   │   ├── 02-pub-sub/
│   │   ├── 03-service/
│   │   ├── 04-action/
│   │   ├── 05-custom-msg/
│   │   └── 06-launch-params/
│   ├── src/               #   TRACK 2: ROS2 colcon workspace
│   ├── launch/            #   Launch files
│   ├── config/            #   YAML config files
│   ├── scripts/           #   Helper scripts
│   ├── docs/              #   Documentation
│   │   └── ERRORS.md
│   ├── logs/              #   Action log
│   │   └── agent-log.md
│   └── tests/             #   Test files
│
└── Menengah ROS2/         # LEVEL 2: (akan datang)
```

---

## Persyaratan / Requirements

**ID:** Yang harus sudah terinstall:

| Kebutuhan | Versi | Cara Cek |
|-----------|-------|----------|
| Ubuntu/Debian (via WSL) | 22.04+ | `cat /etc/os-release` |
| ROS2 | Humble | `source /opt/ros/humble/setup.bash && ros2 --version` |
| Python | 3.8+ | `python3 --version` |
| pip | (ikuti Python) | `pip3 --version` |
| colcon | - | `colcon --version` |
| git | - | `git --version` |

**EN:** Prerequisites:

| Requirement | Version | How to Check |
|-------------|---------|--------------|
| Ubuntu/Debian (via WSL) | 22.04+ | `cat /etc/os-release` |
| ROS2 | Humble | `source /opt/ros/humble/setup.bash && ros2 --version` |
| Python | 3.8+ | `python3 --version` |
| pip | (follows Python) | `pip3 --version` |
| colcon | - | `colcon --version` |
| git | - | `git --version` |

---

## Instalasi / Installation

**ID:** Ikuti langkah ini kalau clone dari GitHub.

**EN:** Follow these steps if cloning from GitHub.

```bash
# 1. Clone repo
git clone https://github.com/<username>/<repo>.git
cd <repo>

# 2. Source ROS2 (WAJIB setiap buka terminal baru)
source /opt/ros/humble/setup.bash
# Atau pakai script yang sudah disediakan:
source Dasar\ ROS2/scripts/source_ros.sh

# 3. Install colcon (kalau belum ada)
sudo apt install python3-colcon-common-extensions

# 4. Verifikasi
ros2 --version
```

---

## Cara Menjalankan / How to Run

**ID:** Di Fase 0 ini belum ada node yang bisa dijalankan. Tapi bisa verifikasi bahwa ROS2 siap:

**EN:** In Phase 0 there are no nodes to run yet. But you can verify ROS2 is ready:

```bash
# Step 1: Source ROS2 dulu (Always source ROS2 first!)
source "Dasar ROS2/scripts/source_ros.sh"

# Step 2: Cek versi ROS2 (Check ROS2 version)
ros2 --version

# Step 3: Lihat daftar node ROS2 (yang sedang berjalan)
# (belum ada karena belum ada node yang jalan)
ros2 node list
```

**ID:** Setelah Fase 1, kamu bisa menjalankan node seperti ini:

**EN:** After Phase 1, you can run nodes like this:

```bash
# Track 1 — Langsung pakai Python
python3 "Dasar ROS2/explore/01-minimal-node/minimal_node.py"

# Track 2 — Pakai ROS2 package (nanti / later)
cd "Dasar ROS2/src"
colcon build
source install/setup.bash
ros2 run ros2_basics talker_node
```

---

## ROS2 Graph Overview

**ID:** Ini akan diisi seiring bertambahnya node. Nanti kamu bisa lihat sendiri visualnya pakai `rqt_graph`:

**EN:** This will be filled as nodes are added. You can see the visual later with `rqt_graph`:

```bash
# Setelah ada node yang jalan / After nodes are running
rqt_graph
```

---

## Tips Debugging / Debugging Tips

**ID:** Error umum dan solusinya ada di `Dasar ROS2/docs/ERRORS.md`.

**EN:** Common errors and solutions are in `Dasar ROS2/docs/ERRORS.md`.

| Masalah / Issue | Penyebab / Cause | Solusi / Solution |
|----------------|-------------------|-------------------|
| `ros2: not found` | Belum source | `source "Dasar ROS2/scripts/source_ros.sh"` |
| `No module named 'rclpy'` | Belum source | `source "Dasar ROS2/scripts/source_ros.sh"` |
| `package not found` | Belum build / source | `colcon build` + `source install/setup.bash` |
| Topic tidak muncul | Node belum publish / crash | Cek terminal, pastikan callback aktif |

---

## Catatan Belajar / Learning Notes

**ID:** Berikut konsep ROS2 yang akan dipelajari di proyek ini:

**EN:** Here are ROS2 concepts that will be learned in this project:

| # | Konsep / Concept | Analogi / Analogy | Folder |
|---|-----------------|-------------------|--------|
| 1 | **Node** | Seorang pekerja di pabrik / A worker in a factory | `Dasar ROS2/explore/01-minimal-node` |
| 2 | **Publisher** | Orang yang nempel pengumuman / Someone posting an announcement | `Dasar ROS2/explore/02-pub-sub` |
| 3 | **Subscriber** | Orang yang baca pengumuman / Someone reading the announcement | `Dasar ROS2/explore/02-pub-sub` |
| 4 | **Topic** | Papan pengumuman / A bulletin board | `Dasar ROS2/explore/02-pub-sub` |
| 5 | **Service** | Minta tolong — "Tolong jumlahkan 2+3" / Asking for help — "Please add 2+3" | `Dasar ROS2/explore/03-service` |
| 6 | **Action** | Minta tolong + laporan progres / Asking for help with progress updates | `Dasar ROS2/explore/04-action` |

---

## Progres / Progress

| Fase / Phase | Konsep / Concept | Status |
|-------------|-----------------|--------|
| 0 | Inisialisasi proyek / Project initialization | ✅ Selesai |
| 1 | Node Dasar + Publisher/Subscriber | ⏳ Belum |
| 2 | Service & Client | ⏳ Belum |
| 3 | Action | ⏳ Belum |
| 4 | Custom Interface (.msg / .srv) | ⏳ Belum |
| 5 | Launch File & Parameter | ⏳ Belum |
| 6 | Integrasi penuh di workspace | ⏳ Belum |

---

## Lisensi / License

**ID:** Proyek ini dibuat untuk tujuan edukasi. Bebas digunakan, dipelajari, dan dimodifikasi.

**EN:** This project is created for educational purposes. Free to use, study, and modify.
