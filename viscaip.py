# Minimal module to control a PTZ camera over Visca Protocol via TCP
import socket
from time import sleep

hostAddress = "192.168.1.253"
hostPort= "1259"
defaultTiltSpeed = 14
defaultPanSpeed = 14

viscaProtocol = {
    "CAM_Address" : b"\x81\x01",
    "CAM_ProtocolEnd" : b"\xFF",
    "CAM_PowerOn" : b"\x04\x00\x02",
    "CAM_PowerOff" : b"\x04\x00\x03",
    "CAM_PanTiltDrive" : b"\x06\x01",
    "CAM_DirectionUP" : b"\x03\x01",
    "CAM_DirectionDOWN" : b"\x03\x02",
    "CAM_DirectionLEFT" : b"\x01\x03",
    "CAM_DirectionRIGHT" : b"\x02\x03",
    "CAM_DirectionSTOP" : b"\x03\x03",
    "CAM_ZoomTELE" : b"\x04\x07\x02", 
    "CAM_ZoomWIDE" : b"\x04\x07\x03", 
    "CAM_ZoomSTOP" : b"\x04\x07\x00"
}

def sendByteCode(cameraAddress,cameraPort,protocolData):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        protocolData = viscaProtocol["CAM_Address"] + protocolData + viscaProtocol["CAM_ProtocolEnd"]
        #print(str(protocolData))
        s.connect((cameraAddress, int(cameraPort)))
        s.sendall(protocolData)
        data = s.recv(1024)
        s.close()
    return data
    
def configCamera(address, port):
    hostAddress = address
    hostPort = port

def command(strCommand,intTiltSpeed=defaultTiltSpeed,intPanSpeed=defaultPanSpeed):
    if strCommand in viscaProtocol:
        #print("Sending " + strCommand + " to " + hostAddress + " at port " + hostPort)
        dataPack = viscaProtocol[strCommand]
        if strCommand in ["CAM_DirectionDOWN", "CAM_DirectionLEFT","CAM_DirectionRIGHT","CAM_DirectionUP","CAM_DirectionSTOP"]:
            dataPack = viscaProtocol["CAM_PanTiltDrive"] + bytes([intPanSpeed]) + bytes([intTiltSpeed]) + viscaProtocol[strCommand]
        feedback = sendByteCode(hostAddress,hostPort,dataPack)
    return feedback

def testCamera():
    # Wiggle the camera
    print(command("CAM_DirectionLEFT"))
    sleep(0.2)
    command("CAM_DirectionSTOP")
    command("CAM_DirectionUP")
    sleep(0.4)
    command("CAM_DirectionSTOP")
    command("CAM_DirectionRIGHT")
    sleep(0.4)
    command("CAM_DirectionSTOP")
    command("CAM_DirectionDOWN")
    sleep(0.6)
    command("CAM_DirectionSTOP")
    command("CAM_DirectionLEFT")
    sleep(0.2)
    command("CAM_DirectionSTOP")
    command("CAM_DirectionUP")
    sleep(0.2)
    command("CAM_DirectionSTOP")
    