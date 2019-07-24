import json
import sys
import ethernetprotocolapi
import time

#path = str(sys.argv)[0]
#ip = str(sys.argv)[1]
#port = str(sys.argv)[2]

path = "C:/Users/Tomás/Documents/Kayto/timeline1.ktmf"
ip = "169.254.102.73"
port = 9993

def main(timeline):
    #ethernetprotocolapi.play(ip, port) dar play ao primeiro da timeline depois ficar a espera que ele acabe e so on e so forth
    loadedClips = ethernetprotocolapi.diskList(ip, port).decode().splitlines()[6:][:-1]
    #for clip in loadedClips

    loadedClipId = ethernetprotocolapi.transportInfo(ip, port).decode().splitlines()[8][9:]
    #timecode = ethernetprotocolapi.clipsGetId(ip, port, int(clipId)).decode("utf-8").splitlines()[6][-11:] #get currently playing clip's duration
    # Traduzir time code para segundos e time.sleep esses segundos e repetir o loop, sys.exit quando acabar
    print(loadedClips)
    print(loadedClipId)
    #ethernetprotocolapi.play(ip, port)

with open(path, "r") as f:
    timeline = f.read()
main(timeline)
