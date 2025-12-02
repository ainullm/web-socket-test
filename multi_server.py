# single_client_web_server.py - VERSI FINAL
import socket
import os

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

def start_single_server(port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"✅ Single-client server berjalan di port {port}...")
    print(f"📁 Direktori kerja: {os.getcwd()}")
    print("=" * 50)

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"🔗 Terhubung dengan {addr}")
        
        try:
            request = connection_socket.recv(1024).decode()
            print(f"📥 Request:\n{request[:200]}...")
            
            # Parse request untuk dapat nama file
            lines = request.split('\n')
            if len(lines) > 0:
                parts = lines[0].split()
                if len(parts) > 1:
                    filename = parts[1]
                    if filename == '/':
                        filename = '/index.html'
                else:
                    filename = '/index.html'
            else:
                filename = '/index.html'
            
            # Debug
            filepath = '.' + filename
            print(f"[DEBUG] Mencari file: {filepath}")
            
            # Coba buka file
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                # Tentukan Content-Type
                content_type = get_content_type(filename)
                response_header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
                
                connection_socket.send(response_header.encode() + content)
                print(f"[SUCCESS] File {filename} dikirim (Content-Type: {content_type})")
                
            except FileNotFoundError:
                # Kirim 404 Not Found
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 - File Not Found</h1>"
                connection_socket.send(response.encode())
                print(f"[ERROR] File {filename} TIDAK ditemukan")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            connection_socket.close()
            print(f"✅ Koneksi dengan {addr} ditutup.\n")

if __name__ == "__main__":
    start_single_server()