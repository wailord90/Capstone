import serial

# next, we will need to start a connection to
# the serial port
exp.trigger = serial.Serial('COM1')

# finally, we want to make sure that the
# connection to the serial port will be stopped
# when the experiment is aborted or finished
exp.cleanup_functions.append(exp.trigger.close)


if(user)