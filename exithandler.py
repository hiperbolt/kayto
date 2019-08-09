import ethernetprotocolapi
import sys

ip = str(sys.argv[1])
port = str(sys.argv[2])

ethernetprotocolapi.stop(ip, port)
ethernetprotocolapi.playRange(ip, port, "clear")
