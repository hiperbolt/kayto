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

def quit(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(b"quit\n")
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
            s.send(b"slot info\n")
            time.sleep(0.1)
            currSlot = s.recv(2024).decode("utf-8").splitlines()[5][-1:]
            if int(currSlot) == 1:
                s.send(b"slot select: slot id: 2\n")
            elif int(currSlot) == 2:
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

def goToClipId(ip, port, clipId):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((str(ip), int(port)))
        s.send(("goto: clip id: %d\n" % clipId).encode())
        time.sleep(0.1)
        data = s.recv(1024)
        s.close()
        return data
    except:
        return "err"

def playRange(ip, port, mode, clipId=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if mode == "set":
        try:
            s.connect((str(ip), int(port)))
            s.send(("playrange set: clip id: %d\n" % clipId).encode())
            time.sleep(0.1)
            data = s.recv(1024)
            s.close()
            return data
        except:
            return "err"
    elif mode == "clear":
        try:
            s.connect((str(ip), int(port)))
            s.send(("playrange clear\n").encode())
            time.sleep(0.1)
            data = s.recv(1024)
            s.close()
            return data
        except:
            return "err"
    else:
        return "wrong mode"
