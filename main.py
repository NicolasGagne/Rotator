
# From:https://adventurist.me/posts/0136
#!/usr/bin/env python

import socket
from rotator import Rotator
from read_arguments import read_arguments
import threading
import sys


#read arguments form the cmd return TCP_IP, TCP_PORT, BUFFER_SIZE

TCP_IP, TCP_PORT, BUFFER_SIZE, test_mode = read_arguments(sys.argv)

if test_mode == "store_false":
    print('Rotator server is starting...')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))

    print('Server started on host: {host} port: {port} \nWaiting for client connection...'
          .format(host=TCP_IP, port=TCP_PORT))

    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)


    my_rotator = Rotator()

    #start thread to keep the rotator moving.
    # Create a stop event
    stop_event = threading.Event()
    thread_my_rotator_moveRotator = threading.Thread(target=my_rotator.moveRotator, args=(stop_event,))
    thread_my_rotator_moveRotator.start()

    while 1:
        try:
            data = conn.recv(BUFFER_SIZE).decode()

            if not data:
                break
            print("Received data:", data.replace("\n", " "))

            if data == "q\n":
                print("Close command, shutting down")
                conn.close()
                exit()
                break
            else:
                try:
                    resp = my_rotator.readServerData(data)
                    print("Send data: ", resp.replace("\n", " "))
                    conn.send(resp.encode())
                except AttributeError:
                    conn.send(" ".encode())

            if not thread_my_rotator_moveRotator.is_alive():
                print('Rotator thread has stop')
                break

        except KeyboardInterrupt:
            stop_event.set()
            break


    print('Disconnection address:', addr)

else:
    print ("Rotator in test_mode")

    my_rotator = Rotator()

    # start thread to keep the rotator moving.
    # Create a stop event
    stop_event = threading.Event()
    thread_my_rotator_moveRotator = threading.Thread(target=my_rotator.moveRotator, args=(stop_event,))
    thread_my_rotator_moveRotator.start()

    while True:

        try:

            cmd = input("Enter P to move the Rotator or p to get the actual position or q to quit: ")

            if cmd == "q":
                stop_event.set()
                break
            elif cmd == "p":
                data = cmd+"\n"
            elif cmd == "P":
                az = float(input("Enter the desire azimute 0 to 360 degrees: "))
                if not (0 <= az <= 359):
                    raise ValueError
                el = float(input("Enter the desire elevation 0 to 90 degrees: "))
                if not (0 <= el <= 90):
                    raise ValueError
                data= str(cmd + " " + str(az) + " " + str(el))
            else:
                raise ValueError

            resp = my_rotator.readServerData(data)

            print('Responce form Rotator:', resp)

            if not thread_my_rotator_moveRotator.is_alive():
                print('Rotator thread has stop')
                break

        except ValueError:
            print("Invalid input. Please enter a valid arguments.")



    print("Exiting test_mode")