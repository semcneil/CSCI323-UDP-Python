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

def main(ipAddr='127.0.0.1', portNum=12001, name='bob', timeout=1, doBeep=True):
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
    doBeep : bool
        Beeps when receives a packet if True
    """
    server_name = ipAddr
    server_port = portNum
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(timeout)  # timeout after 1 second
    try:
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
                if doBeep:
                    play_tone(frequency=2000, duration=0.2)
            while(reply):
                try:
                    reply,server_address = client_socket.recvfrom(2048) # max buffer size 2048
                except TimeoutError:
                    print("Reception timedout")
                    break
                else:
                    print(reply.decode())
                    if doBeep:
                        play_tone(frequency=2000, duration=0.2)
    except KeyboardInterrupt:
        print("Stopping Client")
    finally:
        client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple UDP server. Surround the IP address with double quotes, but leave the port as just an integer.")
    parser.add_argument("-a", "--ipaddr", default="127.0.0.1", help="The IP address the server runs on")
    parser.add_argument("-p", "--port", type=int, default=12001, help="The UDP port for the server to attach to")
    parser.add_argument("-n", "--name", default="Bob", help="The name the server gives in the response")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="The timeout for waiting for another UDP packet")
    parser.add_argument("-b", "--beep", action="store_true", help="pass flag to make it beep")
    args = parser.parse_args()
    main(ipAddr=args.ipaddr, portNum=args.port, name=args.name, timeout=args.timeout, doBeep=args.beep)