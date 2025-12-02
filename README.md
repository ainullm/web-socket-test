# 🖥️ Web Socket Programming Assignment

**Tugas Ujian Akhir Semester - Komunikasi & Jaringan Komputer**  
*Politeknik Elektronika Negeri Surabaya - Program Magister Terapan*

## 📚 Deskripsi
Implementasi web server socket programming dari buku **Computer Networking: A Top-Down Approach** (Kurose & Ross) Chapter 1. Tugas ini terdiri dari dua versi server: **single-client** dan **multi-client concurrent**.

## 🎯 Tujuan Assignment
1. Membuat web server yang melayani single client request
2. Mengembangkan menjadi web server concurrent yang melayani multiple clients
3. Memahami perbedaan antara sequential dan concurrent processing

## 🚀 Fitur
### ✅ Single-Client Server
- Sequential processing (satu client per waktu)
- Support file HTML, TXT, dan lainnya
- HTTP/1.1 compliance
- Error handling (404, 403, 500)

### ✅ Multi-Client Server  
- Concurrent processing dengan threading
- Bisa handle multiple clients bersamaan
- Thread-safe dengan locking mechanism
- Logging informatif dengan thread tracking

## 📁 Struktur File
```
web-socket-test/
│
├── single_client_web_server.py    # Single-client server
├── multi_client_web_server.py     # Multi-client concurrent server
├── index.html                     # Halaman testing HTML
├── test.txt                       # File testing TXT
└── README.md                      # Dokumentasi ini
```

## 🛠️ Cara Penggunaan

### **1. Persiapan**
```bash
# Clone repository
git clone https://github.com/ainullm/web-socket-test.git
cd web-socket-test

# Pastikan Python 3.x terinstall
python --version
```

### **2. Menjalankan Single-Client Server**
```bash
# Jalankan server
python single_server.py

# Server akan berjalan di port 8080
# Output: Server berjalan di port 8080...
```

### **3. Testing Single-Client Server**
```bash
# Test dengan curl
curl http://localhost:8080/
curl http://localhost:8080/test.txt
curl http://localhost:8080/file-tidak-ada.html

# Atau buka browser:
# http://localhost:8080/
```

### **4. Menjalankan Multi-Client Server**
```bash
# Jalankan server concurrent
python multi_server.py

# Server akan berjalan di port 8080
# Output: Multi-Client Web Server ready...
```

### **5. Testing Concurrent Server**
```bash
# Test dengan multiple clients bersamaan
curl http://localhost:8080/ &
curl http://localhost:8080/test.txt &
curl http://localhost:8080/ &

# Atau buka 3 tab browser, akses bersamaan
# http://localhost:8080/
```

## 📊 Perbedaan Single vs Multi Server

| Karakteristik | Single-Client | Multi-Client |
|--------------|---------------|--------------|
| **Arsitektur** | Sequential loop | Threading |
| **Kapasitas** | 1 client per waktu | Multiple clients bersamaan |
| **Performance** | Lambat jika banyak client | Cepat, handle concurrent |
| **Log Output** | Tidak ada thread ID | Thread ID per connection |
| **Use Case** | Learning/Testing | Production-ready |

## 🔧 Testing Concurrent (Advanced)

### **Test dengan Script Python:**
Buat file `test_concurrent.py`:
```python
import threading
import requests

def test_request(url, name):
    print(f"[{name}] Starting...")
    r = requests.get(url)
    print(f"[{name}] Done: {r.status_code}")

urls = [
    ("http://localhost:8080/", "Req-1"),
    ("http://localhost:8080/test.txt", "Req-2"),
    ("http://localhost:8080/", "Req-3")
]

threads = []
for url, name in urls:
    t = threading.Thread(target=test_request, args=(url, name))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

Jalankan:
```bash
python test_concurrent.py
```

### **Hasil Testing Concurrent yang Berhasil:**
```
[DEBUG] Thread-1 akan delay 1.3 detik
[DEBUG] Thread-2 akan delay 1.6 detik
[DEBUG] Thread-3 akan delay 1.0 detik
🧵 THREAD-001 | Total aktif: 3  ← 3 THREAD AKTIF BERSAMAAN!
```

## 📝 Contoh Output Log

### **Single-Client Log:**
```
[14:30:25] 📍 KONEKSI BARU
   ├─ IP Client: 127.0.0.1
   ├─ Method: GET
   ├─ Path: /
   ✅ SELESAI (Waktu: 1.0 ms)
```

### **Multi-Client Log:**
```
[17:30:14.950] 🧵 THREAD-001 | 🌐 KONEKSI BARU
   ├─ Status: 🟢 ACTIVE (Total aktif: 3)
   ├─ Client IP: 127.0.0.1
   📤 RESPONSE: ✅ 200 OK (Durasi: 997 μs)
```

## 🧪 Hasil Testing yang Berhasil

1. ✅ **Single-client**: Melayani request secara berurutan
2. ✅ **Multi-client**: Handle 6+ threads aktif bersamaan  
3. ✅ **Content-Type**: text/html untuk HTML, text/plain untuk TXT
4. ✅ **Error Handling**: 404, 403, 500 responses
5. ✅ **Concurrency Proof**: "Total aktif" mencapai 6 threads

## 📋 File Testing yang Diperlukan

### **index.html**
```html
<!DOCTYPE html>
<html>
<head><title>Test Server</title></head>
<body><h1>Hello from Web Server!</h1></body>
</html>
```

### **test.txt**
```
Ini adalah file teks untuk testing.
Web server concurrent berhasil!
```

## 📚 Spesifikasi Teknis

- **Bahasa**: Python 3.x
- **Protocol**: HTTP/1.1
- **Port Default**: 8080
- **Concurrency Method**: Threading
- **Thread Safety**: Locking dengan `threading.Lock`

## 📄 Lisensi
Tugas Akademik - Politeknik Elektronika Negeri Surabaya

## 👨‍💻 Author
**Ainul M.**  
*Magister Terapan Teknik Informatika & Komputer*  
*Politeknik Elektronika Negeri Surabaya*

---

## 🔗 Link Penting
- Repository: https://github.com/ainullm/web-socket-test
- Referensi: Computer Networking: A Top-Down Approach (Kurose & Ross)
