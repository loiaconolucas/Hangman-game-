from socket import *
from sys import argv
import time


def main():
    if len(argv) != 3 or not argv[2].isdigit():
        print("usage: python3 client.py <server name> <server port>")
    return 1


hostname, serverTCPPort = argv[1], int(argv[2])
print("Client is running...")
print("Remote host: {}, remote TCP port: {}".format(hostname, serverTCPPort))

# Prompt user for their name
while True:
    hello = input("Type hello to start the game\n")
    username = input("Please enter your name: ")
    if hello == "hello":
        break

    else:
        print("Please try again")

# Create TCP socket
serverAdress = (hostname, serverTCPPort)
clientSocket = socket(AF_INET, SOCK_STREAM)


# Connect to the server program
clientSocket.connect(serverAdress)

# Send hello message to the server over TCP connection
hellomsg = hello + " " + username
clientSocket.send(hellomsg.encode("utf-8"))

# TCP Loop
while True:
    # Read in from TCP port
    # we receive the gameport message and use it to later establish a UDP connection to the server

    UDPservername = "localhost"
    gameport = clientSocket.recv(1024)
    decoded = gameport.decode("utf-8")
    print(gameport)

    Udpaddress = "localhost", int(decoded[-6:-1])
    print("connecting via UDP to port ", Udpaddress)
    break
# Create a UDP socket
Udpclientsocket = socket(AF_INET, SOCK_DGRAM)
end = False  # default nd flag

# Game loop
while True:
    # Prompt

    valid_commands = ['start', 'end', 'guess', 'exit']
    print("Please input valid_commands")
    print(valid_commands)
    message = input("")

    if message == "start":
        message = "ready" # we send ready message to server to start the game
        active = True
        Udpclientsocket.sendto(message.encode(), Udpaddress)
        data, addr = Udpclientsocket.recvfrom(2048)
        datamsg = data.decode("utf-8")

        print(datamsg)
        print ("-------------Game Started --------------" )

        while active == True:
            valid_commands = ['end', 'guess', 'exit'] # we only allow these commands during game plauy
            print (valid_commands)
            message = input("") # client program takes in command and sends it to server receives and is ready for a reponse
            Udpclientsocket.sendto(message.encode("utf-8"), Udpaddress)
            data, addr = Udpclientsocket.recvfrom(2048)
            datamsg = data.decode("utf-8")
            i =0
            if message[0:5] == "guess":
                Udpclientsocket.sendto(message.encode("utf-8"), Udpaddress)
                print('sent guess ')
                print(datamsg)
                i += 1 # we use a counter varible to keep track of the amount of tires
                if i >5:
                    print ("You loose") #loosing conditions
                break

    elif message == "end": # end command ends the current game
        print ("Client would like to end game ")
        Udpclientsocket.close()
        break
    elif message == "exit":   # exit command shuts down the client and the program
        exitMsg = "disconnecting and ending game "
        print("\nClient Shutting Down.....")
        time.sleep(3.00)

        Udpclientsocket.close()
        exit(1)
    else:
        print("please enter valid command ")
        print(valid_commands)





print("Closing TCP and UDP sockets...")


#####
if __name__ == "__main__":
    main()
