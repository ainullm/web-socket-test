# test_concurrent_requests.py
import threading
import socket
import time

def send_request(thread_id):
    print(f"[Client-{thread_id}] Mengirim request...")
    
    # Buat socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    
    # Kirim HTTP request
    request = f"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(request.encode())
    
    # Terima response
    response = client_socket.recv(4096).decode()
    
    print(f"[Client-{thread_id}] Response diterima")
    client_socket.close()

# Buat 5 client bersamaan
threads = []
for i in range(5):
    t = threading.Thread(target=send_request, args=(i+1,))
    threads.append(t)
    t.start()

# Tunggu semua selesai
for t in threads:
    t.join()