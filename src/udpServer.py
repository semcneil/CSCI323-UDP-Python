"""
udpServer.py
====================================
This is an example of running a UDP server in Python. Note that the IP address in the
server_socket.bind command must be a valid address. Use 127.0.0.1 for initial testing
since all computers have this set as localhost.

| Author: Seth McNeill
| Date: 2026 October 07
"""

from socket import *
from time import sleep
import argparse

# import beep generation if sound is available
try:
    import sounddevice as sd   # for creating beep
except OSError:  # catch if audio not available (like on virtual host)
    def play_tone(frequency=1000, duration=0.2, sample_rate=44100):
        pass
else: 
    import numpy as np         # for creating beep

    def play_tone(frequency=1000, duration=0.2, sample_rate=44100):
        """Generates and plays a pure sine wave beep entirely in memory.

            Parameters
            ----------
            frequency : int
                Frequency of sine wave for beep
            duration : float
                How long to beep for in seconds
            sample_rate : int
                How fast to sample the sine wave
        """
        # Calculate the time steps
        t = np.linspace(0, duration, int(sample_rate * duration), False)

        # Generate a pure sine wave (values between -1.0 and 1.0)
        wave = np.sin(2 * np.pi * frequency * t)

        # Play the array directly out of your speakers
        sd.play(wave, sample_rate)
        sd.wait()  # Wait until the sound finishes playing

def main(ipAddr='127.0.0.1', portNum=12000, name='alice', nPkt=4, sleepTime=0.2, doBeep=True):
    """
    main function to run the UDP server.

    Parameters
    ----------
    ipAddr : str
        IP Address of the server (your computer or remote server)
    portNum : int
        Port number to open when listening for UDP packets
    name : str
        Name to use when documenting or responding to packets
    nPkt : int
        Number of packets to respond to client with
    sleepTime : float
        Time between packets sent as response to client
    doBeep : bool
        Whether to beep when receiving packets
    """
    server_port = portNum
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((ipAddr, server_port))
    print("The server is ready to receive")
    try:
        while True:
            message, client_address = server_socket.recvfrom(65535)  # will read until buffer empty or 65525 bytes
            print(f'Received: {message.decode()} from {client_address}')
            if(doBeep):
                play_tone(frequency=1000, duration=0.1)
            if(ipAddr != ""):
                for i in range(nPkt):
                    reply = f'server {name} received "{message.decode().upper()}" #{i}'.encode()
                    server_socket.sendto(reply, client_address)
                    sleep(sleepTime)
    except KeyboardInterrupt:
        print("Stopping Server")
    finally:
        server_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple UDP server. Surround the IP address with double quotes, but leave the port as just an integer.")
    parser.add_argument("-a", "--ipaddr", default="127.0.0.1", help="The IP address the server runs on")
    parser.add_argument("-p", "--port", type=int, default=12001, help="The UDP port for the server to attach to")
    parser.add_argument("-n", "--name", default="Alice", help="The name the server gives in the response")
    parser.add_argument("-s", "--sleep", type=float, default=0.2, help="Time to sleep between packets")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of responses to send")
    parser.add_argument("-b", "--beep", action="store_true", help="pass flag to make it beep")
    args = parser.parse_args()
    main(ipAddr=args.ipaddr, portNum=args.port, name=args.name, nPkt=args.count, sleepTime=args.sleep, doBeep=args.beep)
