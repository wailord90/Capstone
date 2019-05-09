#read fingerprint data from #read fingerprint data from serial port and relay information to main logging information
#Andre Britton
import serial
from db_orch from db_orch import query_sessions, query_users, query_footage, import_archive
from SMS import sendText

#initialize serial port for listening
ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

string=""
line2=0
#sendText("working", '+13185371836')
while True:
    for line in ser.read():
        #assemble string 1 asscii character at a time
        string += line
        line2 = ord(line)

        #13= carriage return 10= newline
        if(line2 == 13):
            print(string)
            body=""
            user=""
            #string contain FingerPrint ID# and Confidence Level
            #relay data text message
            
            if (string[11] == '1'):
                body = "Valid Entry: Andre Britton Finger Found"
                user = "Andre"
            if (string[11] == '2'):
                body = "Valid Entry: Darren Johnson Finger Found"
                user = "Darren"
            if (string[11] == '3'):
                body = "Valid Entry: Jeremy Thomas Finger Found"
                user = "Jeremy"
            #SMS
            if(body != ""):
                print("ok")
                #sendText(body, '+13185371836')
                #sendText(body, '+16182075730')
                #sendText(body, '+13184555586')
            change_user(user)

            string = ""

ser.close()
