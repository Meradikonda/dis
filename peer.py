import socket
import random

'''
enter ip address in the format
host(name):port
'''

ip_add = input('IP Address:')

our_host = socket.gethostbyname(socket.gethostname())
our_port = random.randint(2500, 9999)

def init_server(port=our_port,host=our_host):
    
    saddr = (host, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(saddr)
    server.listen(5)
    print(f'[ INIT ] Server started on {host}:{port}')

    return server


def get_peer_ip(message):
    lst = message.split(' ')[-1].split(']')[0].split(':')
    host = lst[0][1:]
    port = int(lst[-1][:-1])
    return (host, port)

def conn_peer(addr:tuple):
    psock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    psock.connect(addr)
    # psock.send('x0D'.encode('utf-8'))
    
def conn_server(ip_add=ip_add):
    host, port = ip_add.split(':')
    ADDR = (host, int(port))
    FORMAT = 'utf-8'

    # connect to central server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDR)
    print(f'[ INFO ] Connected to {ip_add}')

    # sock.close()
    # send peer server details
    sock.sendall(f'x0F peer server ip=> {our_host}:{our_port}'.encode('utf-8'))

    # init server on the peer
    init_server()

     # accept connections
    conn, paddr = init_server().accept()
    conn.setblocking(False)

    
    print(f'[ CONNECTED ] Client connected to the server {ip_add}')

    # elif msg.split(' ')[0] == 'x0D':
    #     print('peer connected')

    while True:
       

        msg = sock.recv(1024).decode(FORMAT)
        print(f'[server] {msg}')

        # get_peer_ip(msg)
        if msg.split(' ')[0] == 'x0H':
            # sock.close()
            phost, pport = get_peer_ip(msg)
            print(f'connecting to server {phost}:{pport}')

        
        msg = str(input('[YOU]>')).lower()

        sock.send(msg.encode(FORMAT))

        if msg == '':
            break

        else:
            msg = sock.recv(1024).decode(FORMAT)
            print(f'[server] {msg}')

    # recv_msg = sock.recv(1024)
    # sock.send(bytes('Received' ,'utf-8'))
    # print(recv_msg.decode('utf-8'))


if __name__=='__main__':
    conn_server()