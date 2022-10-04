import xmlrpc.client as xcl
from xmlrpc.client import ServerProxy, MultiCall
import sys

# from rpc.server_cp import ip_addr


def server_setup(port, host):
    '''
        server setup from xmlrpc
        port: custom defined from ip_addr
        host: from ip_addr() and by the host computer
    '''
    server = ServerProxy(f"http://{host}:{port}")    
    return server


def server_connect(ip_addr:str):

    # server parameters setup

    host, port = ip_addr.split(':')
    server = server_setup(port=port, host=host)

    while True:

        try:
            text = input('[YOU]>').lower()

        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)
        

        if text == '':
            print('Closing down...')
            break
        multi = MultiCall(server)
       
        multi.getInput(text)
     
        for response in multi():
            print(response)
        

    

if __name__=='__main__':
    ip_ad = str(input('IP ADDR:'))
    server_connect(ip_addr=ip_ad)
