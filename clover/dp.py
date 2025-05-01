import socket
import time

IP = '192.168.50.175'
PORT = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


commands = \
    {
      'open':      '1',
      'close':     '2',
      'takeoff':   '3',
      'land':      '4',
      'batka':     '5',
      'off':       '6'
    }


def dport(arg):
    try:
        msg = commands.get(str(arg))
        sock.send(msg.encode("ascii"))
        data = sock.recv(10)
        while not data:
            data = sock.recv(10)
            time.sleep(0.1)
    except Exception:
        print("Ошибка в функции dport ")


if __name__ == '__main__':
    dport('takeoff')
