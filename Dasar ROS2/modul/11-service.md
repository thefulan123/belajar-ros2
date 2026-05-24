# MODUL 11: Service

**TAG:** komunikasi / request-response / sinkron

---

## APA ITU SERVICE?

Service adalah komunikasi **request-response** antara node.

> Service = **memanggil fungsi** di node lain dan **menunggu hasilnya**.

```
Client Node                  Server Node
    │                             │
    ├── request (a=5, b=3) ─────►│
    │                             │  Server menghitung
    │                             │  5 + 3 = 8
    │◄── response (sum=8) ───────┤
    │                             │
```

---

## SERVICE vs TOPIC

| Aspek | Topic | Service |
|-------|-------|---------|
| Arah | Satu arah (broadcast) | Dua arah (request-response) |
| Frekuensi | Terus-menerus | Sekali panggil |
| Blocking | Tidak | Client menunggu |
| Feedback | Tidak | Hanya response akhir |
| Analogi | Radio (siaran) | Telepon (tanya-jawab) |

**Kapan pakai topic?** Data terus-menerus (sensor, kecepatan).

**Kapan pakai service?** Perintah sekali panggil (reset, hitung, simpan).

---

## KENAPA ADA?

### Masalah

Topic hanya broadcast satu arah. Kalau Node A butuh **hasil** dari Node B, topic tidak bisa:

```
Node A ──── "Hitung 5+3" ────► Node B
         (topic tidak punya response)
```

Node A tidak tahu hasilnya. Harus bikin topic terpisah untuk response — rumit.

### Solusi

Service memberikan **request-response** dalam satu paket:

```
Node A ─── request ──► Node B
Node A ◄── response ── Node B
```

Satu panggilan, langsung dapat hasil.

---

## CARA KERJA

### Service Definition

Service punya **request** dan **response**:

```
# AddTwoInts.srv
int64 a           ← request
int64 b           ← request
---
int64 sum         ← response
```

### Server Side

```python
class ServerNode(Node):
    def __init__(self):
        super().__init__('server')
        self.srv = self.create_service(
            AddTwoInts,       # Tipe service
            'add_two_ints',   # Nama service
            self.callback     # Fungsi callback
        )

    def callback(self, request, response):
        # request.a dan request.b dari client
        response.sum = request.a + request.b
        return response  # ← WAJIB return response
```

### Client Side

```python
class ClientNode(Node):
    def __init__(self):
        super().__init__('client')
        self.client = self.create_client(
            AddTwoInts, 'add_two_ints'
        )

        # Tunggu server siap
        while not self.client.wait_for_service(1.0):
            print('Menunggu server...')

        # Buat request
        req = AddTwoInts.Request()
        req.a = 5
        req.b = 3

        # Panggil (async — tidak blocking)
        self.future = self.client.call_async(req)
```

### Alur Lengkap

```
Client                              Server
  │                                    │
  │  create_client(AddTwoInts,         │
  │    'add_two_ints')                 │
  │                                    │
  │  wait_for_service() ──────────────►│  create_service(...)
  │◄────────── siap ──────────────────┤
  │                                    │
  │  call_async(request) ────────────►│  callback(req, res)
  │                                    │  res.sum = req.a + req.b
  │◄────────── response ──────────────┤
  │                                    │
  │  future.result() = sum=8           │
```

### CLI — Memanggil Service

Tanpa coding, service bisa dipanggil langsung dari terminal:

```bash
ros2 service call /add_two_ints \
  example_interfaces/srv/AddTwoInts \
  "{a: 10, b: 20}"
# Output: sum=30
```

---

## CONTOH PENGGUNAAN NYATA

| Service | Fungsi |
|---------|--------|
| `/reset_odometry` | Reset posisi robot ke 0 |
| `/set_led_color` | Ganti warna LED |
| `/save_map` | Simpan peta SLAM |
| `/get_robot_info` | Minta informasi robot |
| `/set_target` | Set target tujuan |

---

## COBA INI

**Eksperimen 1 — Jalankan server dulu:**
```bash
python3 service_server.py  # Terminal 1
python3 service_client.py  # Terminal 2 → langsung sukses
```

**Eksperimen 2 — Client dulu:**
```bash
python3 service_client.py  # Terminal 1 → "Menunggu..."
# Terminal 2: jalankan server
# Client akan langsung terhubung
```

**Eksperimen 3 — Panggil dari CLI:**
```bash
ros2 service list
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 99, b: 1}"
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `wait_for_service` timeout | Server belum jalan | Jalankan server dulu |
| `service type mismatch` | Tipe service salah | Cek dengan `ros2 service type /nama` |
| `future.done() = False` | Belum waktunya | Tunggu atau cek dengan timer |
| Response None | Lupa return | Pastikan `return response` |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 10** — Topic (beda dengan service)
- **Lanjut ke Modul 12** — Action (service + feedback)
- **Praktek: explore/03-service** — implementasi service
