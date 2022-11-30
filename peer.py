import socket
import sys 
import os 
import select
import pickle
import signal
import datetime 
import math
import time 
import random

# global comm info
PEER_CONN_INFO = 'Peer has connected'           # replaces P2P_CHAT_PY_PROTOCOL_HI
PEER_CONN_INFO_ACK = 'PEER CONN ACKD'
PEER_IP_DETS = 'Peer server details'
PEER_TO_PEER_CONN = 'peer to peer conn'
PEER_TRANS_PEER = 'transfering peer'

'''
    GET SERVER DETAILS FROM SERVER OUTPUT(i.e CONSOLE OUTPUT)
'''

# central server details 
cs_ip = input('Enter ip:')
chost, cport = cs_ip.split(':')
caddr = (chost, int(cport))

# setup our own server details
ourPort = random.randint(2000, 5999)
ourHost = socket.gethostbyname(socket.gethostname())

# connect to central server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(caddr)

# create peer server
our_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
our_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
our_server.bind((ourHost, ourPort))
our_server.listen(5)
print(f'[ PEER_INFO ] Server started on {ourHost}:{ourPort}')

# to track all readables
ways_to_rd = [sys.stdin, server, our_server]

# IMPORTANT HELPER FUNCS
def isCommand(msg:str, str_cmd:str):
    return msg.count(str_cmd)

#To print peer table
def print_peer_table( peer_list):
    # os.system('clear')
    # print('Hi '+name+' !\n\n')
    print('\t\t-- Peer table --\n')
    for peer in peer_list:
        # print('+ Name: '+peer[0]+'\t | Port: '+str(peer[1])+' | Ip: '+peer[2]+' | Id_peer: '+str(peer[3]))
        print(peer)
    
def getRandomPeer(peer_list):
    return random.choice(peer_list)

if __name__=='__main__':
    # set up to track peers
    peer_list = []
    my_peer_id = 0

    # track active conn
    active_conn = []
    active_conn_port = []

    # contact the server
    print('[ INFO ] Connecting to central server...')
    server.sendall(pickle.dumps([PEER_CONN_INFO, [ourHost, ourPort]]))

    # main loop
    while True:
        try:
            events_rd,_, _ = select.select(ways_to_rd, [], [])
        except Exception as e:
            print(f'[ WARNING ] Failed due to error {e}')
            break

        for event in events_rd:  

            # get events on our server
            if event is our_server:
                # accept peers to connect to us
                print('[ DEBUG ] Server accepting connections ')
                pconn, paddr = our_server.accept()
                ways_to_rd.append(pconn)
                peer_list.append([paddr[0], paddr[1]])
            
            # get events on central server
            elif event is server:
                try:
                    data = pickle.loads(server.recv(4096))

                    if data:
                        if data[0] == PEER_CONN_INFO_ACK:
                            print(f'Central server said {data[1]}')
                        
                        elif data[0] == PEER_IP_DETS:
                            auxHost, auxPort = data[1]
                            try:
                                aux_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                aux_peer.connect((auxHost, int(auxPort)))

                                if len(peer_list) < 3:                               
                                    aux_peer.send(pickle.dumps([PEER_TO_PEER_CONN, 'Peer connected to you']))
                                    peer_list.append(data[1])
                                    print('[ INFO ] Connected to peer')

                                else:
                                    trans = getRandomPeer(peer_list)
                                    aux_peer.send(pickle.dumps([PEER_TRANS_PEER, trans]))
                                    print(f'[ INFO ] Transferring to {trans}')

                            except Exception as e:
                                print('[ WARNING ] Unable to connect to the server')
                    
                    else:
                        server.close()
                        our_server.close()
                        print('Goodbye  -:)')

                except Exception as e:
                    print(f'Closing beacuse of error {e}')
                    server.close()
                    our_server.close()
                    
                    
            elif event is sys.stdin:
                msg = input()

                if isCommand(msg, '/quit'):
                    pass

                elif isCommand(msg, '/Neighbours'):
                    print_peer_table(peer_list)
                else:
                    print(f'you:{msg}')

            # handle peer connections
            else:
                
                for peer in ways_to_rd:

                    if peer is not server and peer is not our_server and peer is not sys.stdin:
                        try:
                            pdata = pickle.loads(peer.recv(4096))

                            if pdata:
                                if pdata[0] == PEER_TO_PEER_CONN:
                                    print(f' peer {pdata[1]}')
                                print(pdata[1])
                            else:
                                ways_to_rd.remove(peer)
                                peer.close()
                        except Exception as e:
                            print('closing beacuse of error {}'.format(e))
                            peer.close()
                            ways_to_rd.remove(peer)
                            