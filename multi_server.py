# multi_client_web_server.py
import socket
import os
import threading
import time
from datetime import datetime

# Counter untuk thread ID
thread_counter = 0
thread_counter_lock = threading.Lock()
active_threads = 0
active_threads_lock = threading.Lock()

def get_content_type(filename):
    """Menentukan Content-Type berdasarkan ekstensi file"""
    if filename.endswith('.html') or filename == '/':
        return 'text/html'
    elif filename.endswith('.txt'):
        return 'text/plain'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        return 'image/jpeg'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.json'):
        return 'application/json'
    else:
        return 'application/octet-stream'

def get_new_thread_id():
    """Mendapatkan ID unik untuk thread"""
    global thread_counter
    with thread_counter_lock:
        thread_counter += 1
        return thread_counter

def increment_active_threads():
    """Menambah counter thread aktif"""
    global active_threads
    with active_threads_lock:
        active_threads += 1
        return active_threads

def decrement_active_threads():
    """Mengurangi counter thread aktif"""
    global active_threads
    with active_threads_lock:
        active_threads -= 1
        return active_threads

def format_duration(seconds):
    """Format durasi menjadi string yang mudah dibaca"""
    if seconds < 0.001:
        return f"{seconds*1000000:.0f} μs"
    elif seconds < 1:
        return f"{seconds*1000:.1f} ms"
    else:
        return f"{seconds:.2f} s"

def print_server_header(port):
    """Cetak header informasi server"""
    print("=" * 70)
    print("MULTI-CLIENT (CONCURRENT) WEB SERVER")
    print("=" * 70)
    print(f"📂 Direktori kerja  : {os.getcwd()}")
    print(f"🔌 Port server      : {port}")
    print(f"🚦 Status           : READY")
    print(f"📊 Mode             : Multi-Client (Concurrent Threading)")
    print(f"🧵 Max connections  : 5 (listen queue)")
    print("=" * 70)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Server berjalan...")
    print()

def print_connection_start(thread_id, addr, active_count):
    """Cetak info mulai koneksi"""
    client_ip, client_port = addr
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]

    # Increment dulu
    active_count = increment_active_threads()
    
    print(f"[{timestamp}] 🧵 THREAD-{thread_id:03d} | 🌐 KONEKSI BARU")
    print(f"   ├─ Status       : 🟢 ACTIVE (Total aktif: {active_count})")
    print(f"   ├─ Client IP    : {client_ip}")
    print(f"   └─ Client Port  : {client_port}")

def print_request_info(thread_id, request):
    """Cetak informasi request"""
    lines = request.strip().split('\n')
    if lines and len(lines[0].split()) >= 2:
        parts = lines[0].split()
        method = parts[0]
        path = parts[1]
        protocol = parts[2] if len(parts) > 2 else "HTTP/1.1"
        
        print(f"   📥 REQUEST [Thread-{thread_id:03d}]")
        print(f"      ├─ Method    : {method}")
        print(f"      ├─ Path      : {path}")
        print(f"      └─ Protocol  : {protocol}")
        
        # Ambil User-Agent jika ada
        for line in lines:
            if line.lower().startswith('user-agent:'):
                agent = line.split(':', 1)[1].strip()
                print(f"      └─ Client    : {agent[:25]}...")
                break

def print_file_info(thread_id, filename, content_type, file_size):
    """Cetak informasi file"""
    print(f"   📄 FILE INFO [Thread-{thread_id:03d}]")
    print(f"      ├─ Nama file  : {filename}")
    print(f"      ├─ Tipe       : {content_type}")
    print(f"      └─ Ukuran     : {file_size:,} bytes")

def print_response_info(thread_id, status, duration):
    """Cetak informasi response"""
    status_icon = "✅" if status == "200 OK" else "⚠️ " if status == "404 Not Found" else "❌"
    
    print(f"   📤 RESPONSE [Thread-{thread_id:03d}]")
    print(f"      ├─ Status     : {status_icon} {status}")
    print(f"      └─ Durasi     : {format_duration(duration)}")

def print_thread_end(thread_id, active_count):
    """Cetak info akhir thread"""
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    
    print(f"[{timestamp}] 🧵 THREAD-{thread_id:03d} | 📴 KONEKSI SELESAI")
    print(f"   └─ Status       : 🔴 INACTIVE (Total aktif: {active_count})")
    print()

def handle_client(connection_socket, addr):
    """Handle koneksi client dalam thread terpisah"""
    thread_id = get_new_thread_id()

    import random
    delay = random.uniform(1, 3)  # Delay 1-3 detik
    
    print(f"[DEBUG] Thread-{thread_id} akan delay {delay:.1f} detik")
    time.sleep(delay)  # SIMULASI PROSES BERAT
    
    active_count = increment_active_threads()
    
    start_time = time.time()
    
    try:
        # Print info koneksi mulai
        print_connection_start(thread_id, addr, active_count)
        
        # Terima request
        request = connection_socket.recv(4096).decode('utf-8', errors='ignore')
        
        if not request:
            print(f"   ⚠️  REQUEST KOSONG [Thread-{thread_id:03d}]")
            connection_socket.close()
            return
        
        # Print info request
        print_request_info(thread_id, request)
        
        # Parse request
        lines = request.split('\n')
        if lines:
            parts = lines[0].split()
            if len(parts) > 1:
                filename = parts[1]
                if filename == '/':
                    filename = '/index.html'
            else:
                filename = '/index.html'
        else:
            filename = '/index.html'
        
        # Handle request
        try:
            # Buka file
            filepath = '.' + filename
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Tentukan Content-Type
            content_type = get_content_type(filename)
            file_size = len(content)
            
            # Print info file
            print_file_info(thread_id, filename, content_type, file_size)
            
            # Buat response header
            response_header = f"HTTP/1.1 200 OK\r\n"
            response_header += f"Content-Type: {content_type}\r\n"
            response_header += f"Content-Length: {file_size}\r\n"
            response_header += f"Server: Multi-Thread-Python\r\n"
            response_header += f"Connection: close\r\n\r\n"
            
            # Kirim response
            connection_socket.send(response_header.encode() + content)
            
            # Hitung durasi
            end_time = time.time()
            duration = end_time - start_time
            
            # Print response info
            print_response_info(thread_id, "200 OK", duration)
            
        except FileNotFoundError:
            # File tidak ditemukan
            error_content = b"<html><body><h1>404 - File Not Found</h1></body></html>"
            response = f"HTTP/1.1 404 Not Found\r\n"
            response += f"Content-Type: text/html\r\n"
            response += f"Content-Length: {len(error_content)}\r\n\r\n"
            
            connection_socket.send(response.encode() + error_content)
            
            end_time = time.time()
            duration = end_time - start_time
            print_response_info(thread_id, "404 Not Found", duration)
            
        except PermissionError:
            error_content = b"<html><body><h1>403 - Forbidden</h1></body></html>"
            response = f"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n"
            connection_socket.send(response.encode() + error_content)
            
            end_time = time.time()
            duration = end_time - start_time
            print_response_info(thread_id, "403 Forbidden", duration)
            
    except ConnectionResetError:
        print(f"   ❌ KONEKSI DIRESET [Thread-{thread_id:03d}]")
    except Exception as e:
        print(f"   ❌ ERROR [Thread-{thread_id:03d}]: {str(e)[:50]}")
        try:
            error_content = b"<html><body><h1>500 - Internal Server Error</h1></body></html>"
            response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n"
            connection_socket.send(response.encode() + error_content)
        except:
            pass
    finally:
        # Tutup koneksi
        connection_socket.close()
        
        # Update counter
        active_count = decrement_active_threads()
        
        # Print info akhir
        print_thread_end(thread_id, active_count)

def start_concurrent_server(port=8080):
    """Start server dengan concurrent threading"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)  # Queue untuk 5 koneksi
    
    print_server_header(port)
    
    try:
        while True:
            # Terima koneksi baru
            connection_socket, addr = server_socket.accept()
            
            # Buat thread untuk handle client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(connection_socket, addr),
                name=f"ClientHandler-{thread_counter+1}"
            )
            client_thread.daemon = True  # Thread akan mati jika main thread mati
            client_thread.start()
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛑 Server dihentikan oleh user")
    except Exception as e:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ❌ Error server: {e}")
    finally:
        server_socket.close()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Server berhasil dimatikan")
        print(f"📊 Statistik akhir:")
        print(f"   ├─ Total threads dibuat : {thread_counter}")
        print(f"   └─ Threads masih aktif  : {active_threads}")

if __name__ == "__main__":
    start_concurrent_server()