# single_client_web_server.py
import socket
import os
import time

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
    else:
        return 'application/octet-stream'

def print_header():
    """Cetak header informasi server"""
    print("=" * 60)
    print("SINGLE-CLIENT WEB SERVER")
    print("=" * 60)
    print(f"📂 Direktori kerja : {os.getcwd()}")
    print(f"🔌 Port server     : 8080")
    print(f"🚦 Status          : READY")
    print(f"📊 Mode            : Single-Client (Sequential)")
    print("=" * 60)
    print()

def print_connection_info(addr, client_ip, client_port):
    """Cetak info koneksi dengan format rapi"""
    print(f"[{time.strftime('%H:%M:%S')}] 📍 KONEKSI BARU")
    print(f"   ├─ IP Client    : {client_ip}")
    print(f"   ├─ Port Client  : {client_port}")
    print(f"   └─ Alamat Full  : {addr}")

def print_request_info(request):
    """Cetak informasi request"""
    lines = request.split('\n')
    if lines and len(lines[0].split()) > 1:
        method, path, protocol = lines[0].split()[0], lines[0].split()[1], lines[0].split()[2]
        print(f"   📥 REQUEST")
        print(f"      ├─ Method   : {method}")
        print(f"      ├─ Path     : {path}")
        print(f"      └─ Protocol : {protocol}")
        
        # Cari User-Agent
        for line in lines:
            if line.lower().startswith('user-agent:'):
                agent = line.split(':', 1)[1].strip()
                print(f"      └─ Client   : {agent[:30]}...")
                break

def print_response_info(filename, status, content_type=None):
    """Cetak informasi response"""
    print(f"   📤 RESPONSE")
    print(f"      ├─ File       : {filename}")
    print(f"      ├─ Status     : {status}")
    if content_type:
        print(f"      └─ Type       : {content_type}")

def print_error_info(error_msg):
    """Cetak informasi error"""
    print(f"   ❌ ERROR")
    print(f"      └─ Pesan      : {error_msg}")

def print_connection_end(duration_ms):
    """Cetak informasi akhir koneksi"""
    print(f"   ✅ SELESAI (Waktu: {duration_ms:.1f} ms)")
    print()

def start_single_server(port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(1)
    
    print_header()
    
    connection_count = 0
    
    while True:
        try:
            # Tunggu koneksi
            connection_socket, addr = server_socket.accept()
            connection_count += 1
            client_ip, client_port = addr
            
            # Waktu mulai
            start_time = time.time()
            
            print_connection_info(addr, client_ip, client_port)
            
            try:
                # Terima request
                request = connection_socket.recv(4096).decode('utf-8', errors='ignore')
                
                if not request:
                    print("   ⚠️  Request kosong, koneksi ditutup")
                    connection_socket.close()
                    continue
                
                print_request_info(request)
                
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
                    
                    # Kirim response
                    response_header = f"HTTP/1.1 200 OK\r\n"
                    response_header += f"Content-Type: {content_type}\r\n"
                    response_header += f"Server: Single-Client-Python\r\n"
                    response_header += f"Connection: close\r\n\r\n"
                    
                    connection_socket.send(response_header.encode() + content)
                    
                    # Print info response
                    file_size = len(content)
                    print_response_info(filename, "200 OK", content_type)
                    print(f"      └─ Size       : {file_size:,} bytes")
                    
                except FileNotFoundError:
                    # File tidak ditemukan
                    error_content = "<html><body><h1>404 - File Not Found</h1></body></html>"
                    response = f"HTTP/1.1 404 Not Found\r\n"
                    response += f"Content-Type: text/html\r\n"
                    response += f"Server: Single-Client-Python\r\n\r\n"
                    response += error_content
                    
                    connection_socket.send(response.encode())
                    print_response_info(filename, "404 Not Found", "text/html")
                    
                except PermissionError:
                    print_error_info("Permission denied untuk mengakses file")
                    error_content = "<html><body><h1>403 - Forbidden</h1></body></html>"
                    response = f"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n{error_content}"
                    connection_socket.send(response.encode())
                    
            except ConnectionResetError:
                print_error_info("Koneksi direset oleh client")
            except Exception as e:
                print_error_info(str(e))
                try:
                    error_content = "<html><body><h1>500 - Internal Server Error</h1></body></html>"
                    response = f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n{error_content}"
                    connection_socket.send(response.encode())
                except:
                    pass
            
            finally:
                # Tutup koneksi
                connection_socket.close()
                
                # Hitung durasi
                end_time = time.time()
                duration_ms = (end_time - start_time) * 1000
                
                # Print ringkasan
                print_connection_end(duration_ms)
                print(f"[STATISTIK] Total koneksi: {connection_count}")
                print("-" * 60)
                print()
        
        except KeyboardInterrupt:
            print("\n\n🛑 Server dihentikan oleh user")
            break
        except Exception as e:
            print(f"\n❌ Error server: {e}")
            break
    
    server_socket.close()
    print("✅ Server berhasil dimatikan")

if __name__ == "__main__":
    start_single_server()