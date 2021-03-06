# TODO
# * create a log file, log timestamped actions
# * surround 'send's with try-except clauses
# * replace selectors with threads for scalability

import socket
import os
import selectors

BACKLOG = 1024      # size of the queue for pending connections

sel = None          # selector object
s = None            # main socket object

def init_server():
    global s
    global sel

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sel = selectors.DefaultSelector()
    port = 12345                # Reserve a port for your service.
    s.bind(('', port))          # Bind to the port
    s.listen(BACKLOG)           # Now wait for client connection.
    



    print('Server up and running.')


def recv_file(conn, file_name):
    f = open(file_name,'wb')
    l = conn.recv(1024)
    while (l):
        f.write(l)
        l = conn.recv(1024)
    f.close()

def send_file(conn, file_name):
    f = open(file_name, "rb")
    l = os.path.getsize(file_name)
    m = f.read(l)
    conn.send(m)
    f.close()
    conn.shutdown(socket.SHUT_WR)

def test():
    # Server receives file from sender
    c_send, addr_send = s.accept()     # Establish connection with client.
    print ('Got connection from sender:', addr_send)
    recv_file(c_send, 'toexec.py')
    print('file recevied from sender')



    # Server sends file to receiver
    c_rec, addr_rec = s.accept()
    print('Got connection from receiver:', addr_rec)
    send_file(c_rec, 'toexec.py')
    print('file sent to receiver')



    # Server receives output from receiver
    print('receiving file from receiver')
    recv_file(c_rec, 'output.txt')
    print('output file received from receiver')



    # Server sends output to sender
    print('sending output file to sender')
    send_file(c_send, 'output.txt')
    print('output file send to sender')


    # close servers
    c_rec.close()
    c_send.close()

def shutdown_server():
    s.close()
    print('Server shut down.')

def main():
    init_server()
    test()

if __name__ == '__main__':
    main()



# https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
