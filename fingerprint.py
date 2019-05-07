#read fingerprint data from serial port and relay information to main logging information
#Andre Britton
import serial

from SMS import sendText
#initialize serial port for listening
ser = serial.Serial(
    port='COM4',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

string=""
while True:
    for line in ser.read():
        #assemble string 1 asscii character at a time
        string += chr(line)
        #13= carriage return 10= newline
        if(line == 13):
            body=""
            #string contain FingerPrint ID# and Confidence Level
            #relay data text message
            if (string[11] == '1'):
                body = "Valid Entry: Andre Britton Finger Found"
            if (string[11] == '2'):
                body = "Valid Entry: Darren Johnson Finger Found"
            if (string[11] == '3'):
                body = "Valid Entry: Jeremy Thomas Finger Found"
            #SMS
            if(body != ""):
                sendText(body, '+13185371836')
                sendText(body, '+16182075730')
                sendText(body, '+13184555586')
                

            string = ""

ser.close()
