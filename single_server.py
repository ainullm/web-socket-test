# single_client_web_server.py
import socket
import os

def start_single_server(port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"Server berjalan di port {port}...")

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Terhubung dengan {addr}")
        
        try:
            request = connection_socket.recv(1024).decode()
            print(f"Request:\n{request}")
            
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
            
            # Coba buka file
            try:
                with open('.' + filename, 'rb') as f:
                    content = f.read()
                response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                connection_socket.send(response_header.encode() + content)
            except FileNotFoundError:
                # Kirim 404 Not Found
                response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>File Not Found</h1>"
                connection_socket.send(response.encode())
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            connection_socket.close()
            print(f"Koneksi dengan {addr} ditutup.\n")

if __name__ == "__main__":
    start_single_server()