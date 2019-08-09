import json
import sys
import ethernetprotocolapi
import time

path = str(sys.argv[1])
ip = str(sys.argv[2])
port = int(sys.argv[3])

def convertToSeconds(timecode): ## WARNING: HOURS NOT IMPLEMENTED. TIMELINE CLIPS OVER AN HOUR LONG WILL NOT WORK. shit will happen
    convertedTime = 0
    minutes = int(timecode[:2])
    seconds = int(timecode[-2:])
    for i in range(0, minutes):
        convertedTime += 60
    convertedTime += seconds
    return convertedTime

def main(timeline):
    loadedClips = ethernetprotocolapi.diskList(ip, port).decode().splitlines()[6:][:-1]
    if set(eval(timeline)).issubset(loadedClips) == True: #DANGEROUS!! TRUSTING INPUT TO BE CORRECT!! IF THE .KTMF FILE IS CORRUPTED SHIT WILL HAPPEN.
        #IF WE PASS THIS IF STATEMENT, TIMELINE FILE IS VALID
        for i in range(0, len(eval(timeline))): #FOR EACH TL CLIP
            for x in range(0, len(loadedClips)): #FOR EACH DISK CLIP
                #print("Iteration")
                if eval(timeline)[i][3:] == loadedClips[x][3:]: #IF CURRENTLY ITERATED TL CLIP IS THE DISK CLIP
                    #print("playing clip %d" % (int(loadedClips[x][:1])))
                    ethernetprotocolapi.goToClipId(ip, port, int(loadedClips[x][:1]))
                    ethernetprotocolapi.play(ip, port)
                    time.sleep(convertToSeconds(loadedClips[x][:-3][-5:]))
                    ethernetprotocolapi.stop(ip, port)

        #print("exiting")
        ethernetprotocolapi.stop(ip, port)
        ethernetprotocolapi.goToClipId(ip, port, 1)
        ethernetprotocolapi.quit(ip, port)
        sys.exit(0)

with open(path, "r") as f:
    timeline = f.read()
main(timeline)
