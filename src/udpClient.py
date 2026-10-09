"""
udpClient.py
====================================
This is an example of running a UDP client in Python. Note that the IP address in the
server_socket.bind command must be a valid address. Use 127.0.0.1 for initial testing
since all computers have this set as localhost.

| Author: Seth McNeill
| Date: 2026 October 07
"""

from socket import *
import argparse

def main(ipAddr='127.0.0.1', portNum=12001, name='bob', timeout=1):
    """
    main function to run the UDP client.

    Parameters
    ----------
    ipAddr : str
        IP Address of the server (your computer or remote server) to connect to
    portNum : int
        Port number to open when sending UDP packets
    name : str
        Name to use when documenting or sending to packets
    timeout : float
        Time to wait before assuming no more packets are coming in response
    """
    server_name = ipAddr
    server_port = portNum
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(timeout)  # timeout after 1 second
    while(1):
        message = input('Input message: ')
        client_socket.sendto(f"client {name} {message}".encode(), (server_name,server_port))
        if message.lower() == 'bye' or message.lower() == 'quit':
            print("Quitting")
            break
        try:
            reply,server_address = client_socket.recvfrom(2048) # max buffer size 2048
        except TimeoutError:
            print("Receive timed out")
            continue
        else:
            print(reply.decode())
        while(reply):
            try:
                reply,server_address = client_socket.recvfrom(2048) # max buffer size 2048
            except TimeoutError:
                print("Reception timedout")
                break
            else:
                print(reply.decode())
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple UDP server. Surround the IP address with double quotes, but leave the port as just an integer.")
    parser.add_argument("-a", "--ipaddr", default="127.0.0.1", help="The IP address the server runs on")
    parser.add_argument("-p", "--port", type=int, default=12001, help="The UDP port for the server to attach to")
    parser.add_argument("-n", "--name", default="Bob", help="The name the server gives in the response")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="The timeout for waiting for another UDP packet")
    args = parser.parse_args()
    main(ipAddr=args.ipaddr, portNum=args.port, name=args.name, timeout=args.timeout)