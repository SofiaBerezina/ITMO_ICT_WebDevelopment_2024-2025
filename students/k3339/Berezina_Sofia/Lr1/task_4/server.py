import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 14901))
server.listen()

clients, nicknames = [], []

print("Сервер чата запущен")

while True:
    client, addr = server.accept()

    client.send("nickname".encode('utf-8'))

    nickname = client.recv(1000).decode('utf-8')
    nicknames.append(nickname)
    clients.append(client)


    print(f"Новый клиент {nickname}, {addr}")


    def handle_client(client):
        while True:
            # Находим индекс текущего клиента в списке
            index = clients.index(client)
            # Получаем никнейм этого клиента
            nickname = nicknames[index]

            try:
                msg = client.recv(1000).decode('utf-8')
                for c in clients:
                    if c != client:
                        c.send(f"{nickname}: {msg}".encode('utf-8'))
            except:
                if client in clients:
                    clients.remove(client)
                    nicknames.remove(nickname)
                break


    threading.Thread(target=handle_client, args=(client,)).start()