# MODUL 01: Sourcing

**TAG:** infrastruktur / dasar / wajib

---

## APA ITU Sourcing?

Sourcing adalah proses mengaktifkan environment ROS2 di terminal kamu.

Perintahnya:
```bash
source /opt/ros/humble/setup.bash
```

Setelah di-source, terminal kamu "tahu" di mana letak:
- command `ros2`
- library Python `rclpy`
- semua tool ROS2

---

## KENAPA ADA?

### Masalah

Coba jalankan ini tanpa sourcing:
```bash
ros2 --version
```

Hasil:
```
bash: ros2: command not found
```

Kenapa? Karena sistem operasi tidak tahu file `ros2` itu ada di mana.

### Solusi

ROS2 menyimpan semua file executable di folder:
```
/opt/ros/humble/bin/
```

Tapi sistem operasi tidak otomatis mencari ke folder itu. Kita harus bilang ke sistem:

> "Hai, kalau cari command, tolong cek juga di /opt/ros/humble/bin/ ya."

Cara bilangnya: **source** file `setup.bash`.

---

## CARA KERJA

### Environment Variable

Sistem operasi Linux pakai **environment variable** untuk menyimpan pengaturan.

Yang paling penting untuk ROS2 adalah:

| Variable | Fungsi |
|----------|--------|
| `PATH` | Daftar folder tempat sistem mencari command |
| `PYTHONPATH` | Daftar folder tempat Python mencari library |
| `ROS_DISTRO` | Nama distro ROS2 (contoh: humble) |
| `AMENT_PREFIX_PATH` | Daftar folder workspace ROS2 |

### Sebelum Source

```bash
$ echo $PATH
/usr/bin:/bin:/usr/local/bin
```

`ros2` tidak ada di folder-folder itu. Jadi sistem bilang "command not found".

### Sesudah Source

```bash
$ source /opt/ros/humble/setup.bash
$ echo $PATH
/opt/ros/humble/bin:/usr/bin:/bin:/usr/local/bin
```

Sekarang `ros2` ada di PATH. Sistem bisa menemukannya.

### Analogi

Bayangkan `PATH` itu buku telepon. Sebelum source, buku telepon hanya berisi nomor darurat. Sesudah source, kita tambahkan nomor ROS2 ke buku telepon itu.

---

## CONTOH

```bash
# 1. Cek PATH sebelum source
echo $PATH
# Output: /usr/bin:/bin:/usr/local/bin

# 2. Source ROS2
source /opt/ros/humble/setup.bash

# 3. Cek PATH sesudah source
echo $PATH
# Output: /opt/ros/humble/bin:...

# 4. Verifikasi
ros2 --version
# Output: ros2 humble ... (atau sesuai versi)

# 5. Cek distro
echo $ROS_DISTRO
# Output: humble
```

---

## COBA INI

**Eksperimen 1 — Buktikan sourcing itu penting:**

1. Buka **2 terminal**
2. Terminal A: langsung ketik `ros2 node list`
   - Lihat error: `command not found`
3. Terminal B: `source /opt/ros/humble/setup.bash` lalu `ros2 node list`
   - Berhasil: daftar node kosong (tapi tidak error)

**Kesimpulan:** Setiap terminal baru WAJIB di-source. ROS2 tidak otomatis.

**Eksperimen 2 — Lihat perubahan PATH:**

```bash
# Jalankan berurutan
echo "Sebelum:"
echo $PATH
echo ""
source /opt/ros/humble/setup.bash
echo "Sesudah:"
echo $PATH
```

Perhatikan baris `/opt/ros/humble/bin` yang muncul setelah source.

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `ros2: command not found` | Belum source | `source /opt/ros/humble/setup.bash` |
| `ModuleNotFoundError: rclpy` | Belum source | `source /opt/ros/humble/setup.bash` |
| `/opt/ros/humble/setup.bash: No such file` | ROS2 tidak terinstall | Install ROS2 Humble dulu |
| `bash: source: file not found` | Path salah | Cek apakah path-nya benar |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Lanjut ke Modul 02** — Workspace: sourcing juga dipakai untuk workspace lokal
- **Lanjut ke Modul 06** — Source Workspace: kenapa harus source ulang setelah build
