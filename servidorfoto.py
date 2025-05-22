import socket
import threading

# Lista de clientes conectados
clients = []

# Envia dados para todos os clientes, exceto o remetente
def broadcast(sender_socket, data, is_binary=False):
    for client in clients:
        if client != sender_socket:
            try:
                if is_binary:
                    client.sendall(data)
                else:
                    client.send(data)
            except:
                clients.remove(client)
                client.close()

def handle_client(client_socket):
    while True:
        try:
            header = client_socket.recv(1024).decode('utf-8').strip()
            if "<img_size>" in header:
                username, size_info = header.split("<img_size>")
                size = int(size_info)

                # Lê os bytes da imagem
                image_data = b""
                while len(image_data) < size:
                    packet = client_socket.recv(min(size - len(image_data), 4096))
                    if not packet:
                        break
                    image_data += packet

                # Reenvia header + imagem
                broadcast(client_socket, header.encode('utf-8').ljust(1024))
                broadcast(client_socket, image_data, is_binary=True)
            else:
                # Texto comum
                broadcast(client_socket, header.encode('utf-8'))
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server(host="0.0.0.0", port=7000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Servidor inicializado em {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Cliente conectado de {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
