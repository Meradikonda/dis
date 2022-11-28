import socket
import random
import select
import sys
from time import sleep

'''
enter ip address in the format
host(name):port
'''

ip_add = input('IP Address:')


# connect to central server
host, port = ip_add.split(':')      #get th server host, port
cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cserver.connect((host, int(port)))

# create server on the peer
    # get server port and host
our_host = socket.gethostbyname(socket.gethostname())
our_port = random.randint(2000, 9999)
our_addr = (our_host, our_port)

our_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# our_server.setblocking(False)
our_server.bind(our_addr)
our_server.listen()

ways_to_read = [sys.stdin,cserver, our_server]

def get_cserv_ip(cserv:list):
    data = cserv[0]
    ip = data.split(' ')[-1].split(']')[0].split(':')
    phost = ip[0][1:]
    pport = int(ip[-1][:-1])

    return (phost, pport)

# run main func for the peer

if __name__ == '__main__':
    
    # get peer list
    peer_list = []

    # store central server
    cserv_ip = []
    # get active connection
    active_conn = []
    active_conn_sock = []

    # send peer server details to central server
    cserver.sendall(f'x0F peer server ip=> {our_host}:{our_port}'.encode('utf-8'))

    # Main loop
    while True:
        events_rd, events_wr, events_excp = select.select(ways_to_read, [], [])

        for event in events_rd:

            # get our server events
            if event is our_server:
                print(' event on our server received \nAccepting connections')
                
                pconn, paddr = our_server.accept()
                # pconn.setblocking(False)
                ways_to_read.append(pconn)
            
            # get central server events
            elif event is cserver:
                cs_msg = cserver.recv(4096).decode('utf-8')

                if cs_msg:
                    print(f'< SERVER > {cs_msg}')

                    if cs_msg.split(' ')[0] == 'x0H':
                        cserv_ip.append(cs_msg)
                        try:
                            aux_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            aux_peer.connect(get_cserv_ip(cserv_ip))
                            aux_peer.send('connected to xdees'.encode('utf-8'))
                            peer_list.append(aux_peer)
                            print('connected to peer')
                            # cserver.close()
                            # setup chat system 
                            your_msg = input('YOU > ')
                            aux_peer.sendall(your_msg.encode('utf-8'))
                        except Exception as e:
                            print(f' failed to connect with error \n {e}')
                
                else:
                    cserver.close()

            # handle peer events
            else:
                for peer in ways_to_read:
                    
                    if peer is not our_server and peer is not cserver:
                        info = peer.recv(4096).decode('utf-8')

                        if info:
                            print(f'< PEER > {info}')
                            # pmsg = input('YOU>')
                            # peer.sendall(pmsg.encode('utf-8'))
                            # sleep(3)
                        
                        else:
                            ways_to_read.remove(peer)
                            peer.close()