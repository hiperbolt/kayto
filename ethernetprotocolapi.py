import socket
import time

def ping(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"ping\n")
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def play(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"play\n")
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def stop(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"stop\n")
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def record(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"record\n")
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def transportInfo(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"transport info\n")
        a = 0
        while a < 2:
            a = a + 1
            data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def gotoClip(ip, port, move):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        if move == "prev":
            s.send(b"goto: clip id: -1\n")
        elif move == "next":
            s.send(b"goto: clip id: +1\n")
        a = 0
        while a < 2:
            a = a + 1
            data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def clip(ip, port, pos):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        if pos == "start":
            s.send(b"goto: clip: start\n")
        elif pos == "end":
            s.send(b"goto: clip: end\n")
        a = 0
        while a < 2:
            a = a + 1
            data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def diskList(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"disk list\n")
        time.sleep(0.1)
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def toggleSlot(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((str(ip), int(port)))
            # QUESTIONAR SLOT ATIVA PARA DEPOIS FAZER TOGGLE EM RELAÇÃO A ISSO, SLOT ATIVA = currSlot
            if currSlot == 1:
                s.send(b"slot select: slot id: 2\n")
            elif currSlot == 2:
                s.send(b"slot select: slot id: 1\n")
            data = s.recv(1024)
            s.close()
            return data
        except:
            return "err"

def transportInfo(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"transport info\n")
        time.sleep(0.1)
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def clipsGetId(ip, port, clipId):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(("clips get: clip id: %d\n" % clipId).encode())
        time.sleep(0.1)
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"
