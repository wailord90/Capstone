# read fingerprint data from serial port and relay information to main logging information
# Andre Britton
import serial
# initialize serial port for listening
ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)

string = ""
while True:
    for line in ser.read():
        # assemble string 1 asscii character at a time
        string += chr(line)
        # 13= carriage return 10= newline
        if(line == 13):
            #print (string)
            # string contain FingerPrint ID# and Confidence Level
            # relay data to main logging information
            if (string[11] == '1'):
                print("Thumb")
            if (string[11] == '2'):
                print("Index Finger")
            if (string[11] == '3'):
                print("Middle Finger")
            if (string[11] == '4'):
                print("Ring Finger")
            if (string[11] == '5'):
                print("Little Finger")
            string = ""

ser.close()
