import serial

with serial.Serial('COM5') as ser:
    with open('train_data.txt', 'w') as f:
        while True:
            line = ser.readline()
            line = line.rstrip().decode('utf-8')
            print(line)
            f.write((line)+'\n')
