# author: TODO: Kenton Bell
from urllib.parse import urlparse
from random import randint
from scapy.all import *
from socket import gethostbyname
from sys import argv



def main():

    # these show helpful PRINT code for debugging purposes
    # # # # to have nothing run in command line, set all to false
    showTestCode = False

    try:
        ifShowTestCode = argv[2]
        if ifShowTestCode == '-t':
            showTestCode = True
    except:
        pass

    servername = "localhost"


    targetport = 80

    try:
        url = argv[1]
    except:
        print("ERROR: Invalid url. The next argument should be the url.")
        return

    if not url.startswith("http://"):
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"

    url_parsed = urlparse(url)


    if showTestCode:
        # print("flag: " + flag)



        print("url: " + url)

        print("Url Parsed:" + str(url_parsed))


    serverName = url_parsed.hostname
    serverPort = 80
    first_name = "Kenton"
    tcpInitialSequenceNumber = len(first_name)
    tcpInitialSequenceNumber = 6 #or we can hardcode, which I trust more...

    # Step 1 TCP

    tcp = TCP()
    ip = IP()

    tcp.dport = serverPort
    tcp.flags = 'S'
    tcp.seq = tcpInitialSequenceNumber
    # tcp.sport = serverPort
    # tcp.chksum = 0

    #make ip dest
    ip.dst = serverName

    try:
        firstResponse = sr1(ip/tcp)
    except:
        print("ERROR: The first sr1 broke.")
        return


    if showTestCode:
        print("We successfully sent the first packet")

    #send ACK
    # tcp.seq = firstResponse.seq+1
    tcp.seq = 7
    tcp.ack = firstResponse.seq+1
    # tcp.dport = firstResponse.dport #still 80
    tcp.flags = 'A'

    try:
        send(ip/tcp)
    except:
        print("ERROR. The returning ACK packet was not sent.")
        return
    # send ACK



    # 2 make get PA (push/ack) request

    if not url_parsed.path:
        path = "/"
    else:
        path = url_parsed.path

    message = "GET " + path + " HTTP/1.1\r\nHost: " + serverName + "\r\nConnection: close\r\n\r\n"

    if showTestCode:
        print("sending: \n\n" + message)


    #prepare PUSH/ACK
    tcp.flags = 'PA'

    tcp.add_payload(message.encode())


    try:
        send(ip/tcp)
    except:
        print("there was an error with the payload send message")
        return



    # # modifiedMessage = ""
    # # loopCount = 0
    # while True:
    #     # loopCount += 1
    #
    #     response = tcp.recv(2048)
    #
    #     if len(response) == 0:
    #         # print("Loop count: " + str(loopCount) + "")
    #         # print("Closing Connection")
    #         break
    #     modifiedMessage += response.decode()
    #
    # splitMessage = modifiedMessage.split("\r\n") #1 to cut off 200 request
    #
    #
    # headers, body = modifiedMessage.split("\r\n\r\n", 1)
    #
    # print(body)




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




