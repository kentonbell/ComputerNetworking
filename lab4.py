# author: TODO: Kenton Bell
import os
from sys import argv, path
from socket import *
from urllib.parse import urlparse


def main():

    # these show helpful PRINT code for debugging purposes
    # # # # to have nothing run in command line, set all to false
    showTestCode = False

    try:
        ifShowTestCode = argv[4]
        if ifShowTestCode == '-t':
            showTestCode = True
    except:
        pass

    servername = "localhost"

    #this is the input
    try:
        flag = argv[1]
    except:
        print("ERROR: No flag provided. Here are the available flags: -p for printing, -f for outputting. \n   The next argument should be the target port (80 is recommended)\n   The last argument should be the url.")

        return

    printing = False
    outputting = False

    if flag == '-p':
        printing = True
    elif flag == '-f':
        outputting = True
    else:
        print("ERROR: Invalid flag. Here are the available flags: -p for printing, -f for outputting. ")
        return

    try:
        targetport = argv[2]
    except:
        print("ERROR: Invalid target port. The next argument should be the target port (80 is recommended)")
        return
    # targetport = argv[2]

    try:
        url = argv[3]
    except:
        print("ERROR: Invalid url. The next argument should be the url.")
        return

    if not url.startswith("http://"):
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"

    url_parsed = urlparse(url)


    if showTestCode:
        print("flag: " + flag)

        print("targetport: " + targetport)

        print("url: " + url)

        print("Url Parsed:" + str(url_parsed))


    serverName = url_parsed.hostname
    serverPort = int(targetport) #make sure it is an int and 80

    # Step 1 TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # 2

    if not url_parsed.path:
        path = "/"
    else:
        path = url_parsed.path

    message = "GET " + path + " HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: close\r\n\r\n"




    if showTestCode:
        print("sending: \n\n" + message)




    try:
        clientSocket.send(message.encode())
    except:
        print("there was an error with the client socket send message")
        return

    modifiedMessage = ""


    # loopCount = 0
    while True:
        # loopCount += 1

        response = clientSocket.recv(2048)

        if len(response) == 0:
            # print("Loop count: " + str(loopCount) + "")
            # print("Closing Connection Closing Connection Closing Connection Closing Connection Closing Connection Closing Connection")
            break
        modifiedMessage += response.decode()

    splitMessage = modifiedMessage.split("\r\n") #1 to cut off 200 request

    clientSocket.close()

    headers, body = modifiedMessage.split("\r\n\r\n", 1)
    if printing:
        print(body)
    if outputting:
        with open("output.txt", "w") as f:
            f.write(body)



    '''
    try:
        justHTMLOutput = splitMessage[splitMessage.index("<!DOCTYPE HTMLE>") + 0:] #added E to avoid
    except:
        if showTestCode:
            print("there was an error with the just html output.\n\nHere is the split message instead: \n\n" + str(splitMessage))
        try:
            justHTMLOutput = splitMessage[splitMessage.index("<htmEl>") + 0:] #added E to avoid
        except:
            if showTestCode:
                print("there was an error with the just html output AGAINNNNNNNNNN.\n\nHere is the split message instead: \n\n" + str(splitMessage))
            try:
                justHTMLOutput = splitMessage[splitMessage.index("Connection:E close") + 1:] #added E to avoid

            except:
                if showTestCode:
                    print("No html found in the response! Running last case: \n\n")
                # print(str(splitMessage))
                headers, body = modifiedMessage.split("\r\n\r\n", 1)
                if printing:
                    print(body)
                if outputting:
                    with open("output.txt", "w") as f:
                        f.write(body)
                return




    if showTestCode:
        print("\nOUTPUTTiNG\n")

    if outputting:
        with open("output.txt", "w") as f: #overwrites file
            f.write("")

    for line in justHTMLOutput:
        if printing:
            if line:
                print(line)
        if outputting:
            if line:
                with open("output.txt", "a") as f:
                    f.write(line + "\n")



    # print("Here is the response from the server: \n" + str(splitMessage)

    '''




if __name__ == "__main__":
    main()




