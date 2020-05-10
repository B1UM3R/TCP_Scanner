import socket
import argparse
import threading
from queue import Queue

checks = {}
TCP_TIMEOUT = 5
hostPort_queue = None


def ports_parser(buf):
    if "-" in buf:
        res = [int(i) for i in range(int(buf.split('-')[0]), int(buf.split('-')[1]) + 1)]
    else:
        res = [int(buf)]

    return res


def init_parser():
    parser = argparse.ArgumentParser(description="Программа для сканирования TCP-портов. Для запуска необходимо "
                                                 "вписать 2 аргумента: ip адрес, который будем сканировать и "
                                                 "диапазон портов. Пример запуска: scanner.py -p 0-2000 192.168.0.1 "
                                                 "Шершнев Павел КН-202(МЕН-280207)")
    parser.add_argument("ip", type=str, help="Введите ip адрес, который будем сканировать")
    parser.add_argument("-p", type=str, help="Введите номер порта, который будем проверять на доступность, либо "
                                             "диапазон портов через разделитель '-'")

    return parser


def ports_scanner(host, port):
    sock = socket.socket()
    sock.settimeout(TCP_TIMEOUT)

    try:
        sock.connect((host, port))
        checks[host + ":" + str(port)] = 'порт открыт'
    except:
        checks[host + ":" + str(port)] = 'порт закрыт'

    sock.close()


def runner():
    while 1:
        host, port = hostPort_queue.get()
        ports_scanner(host, port)
        hostPort_queue.task_done()


if __name__ == "__main__":

    args = init_parser().parse_args()

    target_ip = args.ip
    ports = ports_parser(args.p)

    hostPort_queue = Queue()

    for _ in range(50):
        thread = threading.Thread(target=runner)
        thread.daemon = True
        thread.start()

    for port in ports:
        hostPort_queue.put((target_ip, port))

    hostPort_queue.join()

    for i in checks:
        if checks[i] == 'порт открыт':
            print(i, checks[i])
