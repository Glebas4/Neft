import socket
import time

IP = '192.168.50.175'
PORT = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

commands = \
    {
      'open':      '1',  //Открытие коробки
      'close':     '2',  //Закрытие коробки
      'takeoff':   '3',  //Открытие коробки и стрелка вверх типо взлет
      'land':      '4', //Открытие коробки и стрелка вниз типо посадка
      'batka':     '5', //Иконка батарейки
      'off':       '6'  //Закрытие коробки и выключение матрицы
    }


def dport(arg):
    msg = commands.get(str(arg))
    sock.send(msg.encode("ascii"))
    data = sock.recv(1)
    while not data:
        data = sock.recv(1)
    #print('DONE')



if __name__=='__main__':  //Все что ниже этой строки срабатывае при запуске программы
    dport('takeoff') //В скобочках пишешь нужную команду и запускаешь прогу
    #dport('off')
    #dport('land')
    #dport('batka')
