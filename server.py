from unicodedata import name
from xmlrpc.server import SimpleXMLRPCServer
# import datetime
import socket
from socketserver import ThreadingMixIn
from datetime import datetime
from tzlocal import get_localzone
from pytz import timezone
import sys

# threading mixin class

class ThreadedXMLRPC(ThreadingMixIn, SimpleXMLRPCServer):pass

def ip_addr():
    port = 6789
    ip = socket.gethostbyname(socket.gethostname())
    server = f'{ip}:{port}'
    return server


def get_time() -> str:
    '''
    Get current time in the format  
    '''

    format = "%a %b %d %H:%M:%S %Z %Y"

    # current UTC time
    now_utc = datetime.now(timezone('UTC'))

    # convert to local time
    now_local = now_utc.astimezone(get_localzone())

    return now_local.strftime(format)


def get_input(time):
    '''
    Get connection from clients and return the formatted date
    '''

    if time.lower() == 'time':
        return get_time()
    else:
        return get_time().upper()


def run():
    host, port = ip_addr().split(':')
    addr = (host, int(port))

    with ThreadedXMLRPC(addr) as server:

        server.register_function(get_input, 'getInput')   
        server.register_multicall_functions()
       
        print(f'[STARTING] server started at {ip_addr()}')

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

if __name__=='__main__':
    run()