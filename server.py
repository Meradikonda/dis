import socket
import random 
import sys
import os
import pickle
import select



# global comm info
PEER_CONN_INFO = 'Peer has connected'           # replaces P2P_CHAT_PY_PROTOCOL_HI
PEER_CONN_INFO_ACK = 'PEER CONN ACKD'
PEER_TRANS_PEER = 'transfering peer'
PEER_IP_DETS = 'Peer server details'

# setup server deatails 

host = socket.gethostbyname(socket.gethostname())
port = random.randint(6000, 9999)
saddr = (host, port)

# setup lists that are required
# socket to read
sockets_rd = [sys.stdin]

# strack all connections 
sock_addr_port = []

# track peers
peers_list = []
id_peer = 1

# IMPORTANT HELPER FUNCTIONS 
def getIpFromSocket(sock_addr:list, sock_rcv):

    for client in sock_addr:
        if client[0] is sock_rcv:
            return client[1]

def get_random_peer(pList:list=peers_list):
    return random.choice(pList)

def isCommand(msg:str, str_cmd):
    return msg.count(str_cmd)

def getMembers(membs_list:list):
    print('\t\t -- Members table -- \n')
    
    for member in membs_list:
        print(member)

'''
    This is the main function that is called whenever the server is 
    started. It creates all the server functionalities such as setting
    up the server listening socket.
    NOTE: Server output its ip address in the format of host:port
    example:
        [ SERVER_INFO ] Server started on 192.168.1.11:9447 
        => the host:port pair is the one that need to be pasted in the 
            peer side when prompted for  central server ip.

'''
def start_server():
     # set up the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(saddr)
    s.listen(5)
    print(f'[ SERVER_INFO ] Server started on {host}:{port} ')

    sockets_rd.append(s)

    # main server loop
    while True:
        try:
            events_rd, _, _ = select.select(sockets_rd, [], [])
        except KeyboardInterrupt:
            os.system('clear')
            print('shutting Down...')

            for sock in sockets_rd:
                sock.close()            
            sys.exit()

        for event in events_rd:

            if event == s:
                conn, paddr = s.accept()
                sock_addr_port.append([conn, paddr[0], paddr[1]])
                sockets_rd.append(conn)

            elif event is sys.stdin:
                msg = input()
                
                if isCommand(msg, '/members'):
                    getMembers(peers_list)

            else:
                # handle other conn
                for sock_to_rcv in sockets_rd:
                    if sock_to_rcv != s and sock_to_rcv is event:
                        data = pickle.loads(sock_to_rcv.recv(4096))

                        if data:
                            if data[0] == PEER_CONN_INFO:
                                
                                # get the first peer and return ack of first peer
                                if len(peers_list) <1:
                                    sock_to_rcv.sendall(pickle.dumps([PEER_CONN_INFO_ACK, 'welcome first peer']))
                                    peers_list.append(data[1])

                                    # # close connection after sending the message
                                    # sock_to_rcv.close()             #look out for this code[POTENTIAL PITFALLS]
                                    # sockets_rd.remove(sock_to_rcv)
                                    # print(f'[ INFO ] CONNETION CLOSED WITH {sock_to_rcv}')
                               
                                # handle when more than one peer
                                else:
                                                                       
                                    # send him ack.
                                    sock_to_rcv.sendall(pickle.dumps([PEER_IP_DETS, get_random_peer()]))
                                    peers_list.append(data[1])

                        else:
                            sock_to_rcv.close()
                            sockets_rd.remove(sock_to_rcv)
                            print(f'[ INFO ] REMOVED {sock_to_rcv} from readable sockets')

if __name__=='__main__':
    start_server()
   


