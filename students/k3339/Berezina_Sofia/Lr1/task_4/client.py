import socket
import threading

sock = socket.socket()
sock.connect(('127.0.0.1', 14901))

def recv_msg():
    while True:
        msg = sock.recv(1000).decode('utf-8')
        if msg == 'nickname':
            print("Введите ваш никнейм: ")
            nickname = input()
            sock.send(nickname.encode('utf-8'))
        else:
            print(msg)

threading.Thread(target=recv_msg).start()

while True:
    msg = input()
    sock.send(msg.encode('utf-8'))