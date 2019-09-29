from socket import *
from sys import argv
from random import *
from game import *


def main():
    # Parse command line args
    if len(argv) != 2:
        print("usage: python3 server.py <word to guess or '-r' for random word>")
        return 1

    print("Server is running...")
    # Create the TCP Socket
    TCPsocket = socket(AF_INET, SOCK_STREAM)
    print("Creating TCP socket...")

    # Bind a port to the TCP socket, letting the OS choose the port number

    TCPsocket.bind(("", 0))

    # Get the port number of the socket from the OS and print it
    print("Server is listening on port", (TCPsocket.getsockname()[1]))
    # The port number will be a command-line parameter to the client program

    # Configure the TCP socket (using listen) to accept a connection request
    TCPsocket.listen(1)

    try:  # try/except to catch ctrl-c
        while True:
            print("Waiting for a client...")
            connectionSocket, addr = TCPsocket.accept()

            # TCP loop
            while True:
                # Continuously Read in from TCP port
                player = connectionSocket.recv(1024)
                decoded = player.decode("utf8")

                print(decoded)

                # Create and bind a UDP socket, letting the OS choose the port number
                print("Creating UDP socket...")

                ServerUDPSocket = socket(AF_INET, SOCK_DGRAM)
                ServerUDPSocket.bind(("", 0))
                # Add a timeout to the UDP socket so that it stops listening
                # after 2 minutes of inactivity
                ServerUDPSocket.settimeout(120)

                # Get the port number assigned by the OS and print to console
                print("UDP Port number : ", ServerUDPSocket.getsockname())
                print(ServerUDPSocket.getsockname())

                # Put the UDP port number in a message and send it to the client using TCP
                print("Sending UDP port number to client using TCP connection...")

                gameport = "Gameport "+ str(ServerUDPSocket.getsockname())
                connectionSocket.send(gameport.encode("utf-8"))

                break
            break
        # Break from loop once needed info is received
        active = False  # game not active by default

        # Game (UDP) loop
        while True:
                try:
                    # Receive data on UDP port
                    clientAddress = ServerUDPSocket.recvfrom(2048)
                    UdpMessage = clientAddress[0].decode('utf-8').lower()
                    clientAddressUdp= clientAddress[1]

                    print("UDP connection established")
                except socket.timeout:  # catch UDP timeout
                 print("Ending game due to timeout...")
                 ServerUDPSocket.close()
                 break  # break and wait to accept another client


                if UdpMessage == "ready": # ready message initializes game
                    # We only allow a one player game
                    if active == True:
                        errMsg = " Serverbusy with another player"
                        print(errMsg)
                        ServerUDPSocket.sendto(errMsg.encode("utf-8"), clientAddressUdp)

                    # Game initialization
                    active = True
                    word, word_blanks, attempts, win = gameSetup(argv)
                    print("Hidden Word: {}".format(word))
                    print("Starting game...")

                    # we create the stat message
                    statMsg = "Word: " + word_blanks + "Attempts Left: " + str(attempts)
                    # we create an instruction message
                    instr = INSTRUCTIONS +"\n" + statMsg
                    ServerUDPSocket.sendto(instr.encode("utf-8"),clientAddressUdp)
                    # We enter a game play loop that initiates once the start message is received


                    clientAddress = ServerUDPSocket.recvfrom(2048)
                    UdpMessage = clientAddress[0].decode('utf-8').lower()
                    clientAddressUdp = clientAddress[1]

                    if UdpMessage[0:5] == "guess":# Gameplay. We extract the last ch from our UDP message variable and store it in a var called guess
                                              # we pass guess into the Game file functions to check if correct guess. we then send the user back the stat command
                        guess = UdpMessage[-1]
                        if win == False:
                            statMsg = "Word: " + word_blanks + "Attempts Left: " + str(attempts)+ "condition: " + str(win)
                            print ("guess is "+ guess)
                            checkGuess(word, word_blanks, attempts,guess, win)
                            ServerUDPSocket.sendto(statMsg.encode("utf-8"), clientAddressUdp) # the stat message gets updated each round and get send back to the client.
                        if win == True:
                            winMsg= "You Win"
                            ServerUDPSocket.sendto(winMsg.win("utf-8"), clientAddressUdp)
                            active = False
                            break


                    elif UdpMessage == "end": # end message terminates the game and return to the start of the UDP loop
                         print ("Ending Game")
                         end = ("Game end")
                         ServerUDPSocket.sendto(end.encode("utf-8"),clientAddressUdp)
                         ServerUDPSocket.close()
                         active=False


                    elif UdpMessage == "exit" :
                        print ("Ending client process ")
                        ServerUDPSocket.close()
                        active=False

                    else: # na command when server gets wrong instruction
                        na = "please input valid command "
                        ServerUDPSocket.sendto(na.encode("utf-8"), clientAddressUdp)


    except KeyboardInterrupt:
# Close sockets
        ServerUDPSocket.close()
        TCPsocket.close()
        print("Closing TCP and UDP sockets...")


###########################################


if __name__ == "__main__":
    main()
