import socket
import threading
import sys

sock = socket.socket()
try:
    sock.connect(('127.0.0.1', 14901))
except ConnectionRefusedError:
    print("Не удалось подключиться к серверу")
    sys.exit(1)

def recv_msg():
    while True:
        try:
            msg = sock.recv(1000).decode('utf-8')
            if not msg:  # Сервер отключился
                print("Сервер отключен")
                break
            if msg == 'nickname':
                print("Введите ваш никнейм: ", end='', flush=True)
                nickname = input()
                sock.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except (ConnectionResetError, OSError) as e:
            print(f"\nСоединение с сервером разорвано: {e}")
            break
        except KeyboardInterrupt:
            break
    # Завершаем программу при разрыве соединения
    sys.exit(0)

# Запускаем поток для приема сообщений
recv_thread = threading.Thread(target=recv_msg)
recv_thread.daemon = True
recv_thread.start()

try:
    while True:
        try:
            msg = input()
            sock.send(msg.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError, OSError):
            print("Соединение с сервером потеряно")
            break
        except KeyboardInterrupt:
            print("\nЗавершение работы клиента")
            break
except KeyboardInterrupt:
    print("\nЗавершение работы клиента")
finally:
    sock.close()