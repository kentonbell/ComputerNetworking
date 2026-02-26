# author: TODO: Kenton Bell


from scapy.all import *
from socket import gethostbyname
from subprocess import getstatusoutput
from sys import argv

from scapy.layers.inet import TCP, ICMP


def main():

    # these show helpful PRINT code for debugging purposes
    # # # # to have nothing run in command line, set all to false
    showTestCode = False

    try:
        ifShowTestCode = argv[3]
        if ifShowTestCode == '-t':
            showTestCode = True
    except:
        pass


    # maxHops = 100
    try:
        maxHops = argv[2]
    except:
        print("ERROR: Invalid maximum hops. The next argument should be the maximum number of hops to allow.")
        return

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


    try:
        serverIP = gethostbyname(url.split("//")[1].split("/")[0])
    except Exception as e:
        print(f"Couldnt resolve hostname! {e}")
        return

    print(f"route to {url.split('//')[1].split('/')[0]} ({serverIP}), {maxHops} hops max")

    if showTestCode:
        print("url: " + url)

    asNumbers = []
    reached_target = False

    for ttl in range(1, maxHops + 1):
        ip = IP(dst=serverIP, ttl=ttl)
        syn = TCP(dport=80, flags='S')



        packet = ip  / syn

        response = sr1(packet, verbose=0, timeout=3)

        if response:
            # if response.haslayer(ICMP) and response[ICMP].type == 11:
            if response.haslayer(TCP) and response[TCP].flags == "SA":
                if showTestCode:
                    print("we have got to the end!")
                    print(response.getlayer(TCP).getlayer(ICMP).payload)
                break
            hopIP = response.src
            print(f"{ttl} - {hopIP}")

            # WHOIS Lookup
            whois_out = getstatusoutput(f"whois -h whois.cymru.com {hopIP}")
            asNum = "***"
            for line in whois_out[1].splitlines():
                if line.strip().startswith("AS") or line.strip()[0].isdigit():
                    parts = line.split("|")
                    if len(parts) > 0 and parts[0].strip().isdigit():
                        asNum = f"AS{parts[0].strip()}"
                        break
            if asNum not in asNumbers and asNum != "***":
                asNumbers.append(asNum)

            if hopIP == serverIP:
                reached_target = True
                break
        else:
            print(f"{ttl} - * * *")

        # Print AS numbers as in the example format
    print("Traversed AS numbers: ", end="")
    for i, asNum in enumerate(asNumbers):
        if i > 0:
            print(" -> ", end="")
        print(asNum, end="")
        if (i + 1) % 3 == 0 and i + 1 < len(asNumbers):
            print(" ->\n", end="")
    



    """

    serverName = gethostbyname(url)
    ip = IP()
    ip.flags = 'S'
    ip.dst = serverName

    asNumumberlist = None
    SourcePortlist = None
    ReverseDNSLoopupList = None
    firstpacket = ip
    hopIndex = 0
    try:
        while hopIndex < maxHops:
            curResponse = sr1(firstpacket, verbose=0, timeout=3)
            if curResponse:
                SourcePortlist += curResponse.src
                curAddress = curResponse.src

                if showTestCode:
                    print(f"curAddress::: {curAddress}")

                whois = getstatusoutput(f"whois -h whois.cymru.com {curAddress}")

                splitWhois = whois[1].split("\n")
                for i in splitWhois:
                    if i.isdigit():
                        asNumumberlist += i.split(" ")[0]

                nsLookup = getstatusoutput(f"nslookup {curAddress}")
                ReverseDNSLoopupList += nsLookup[1].split("name")[1]

                hopIndex += 1
                ip.dst = serverName
                ip.src = curAddress

            else:
                asNumumberlist += "***"
    except:
        print("ERROR: The sr1 hopper broke.")
        return


    if showTestCode:
        print("We successfully sent the first packet")

    index = 0
    print("AS Numbers: ")
    for asNumumber in asNumumberlist:
        print(f"{index}: {asNumumber}")

    """


if __name__ == "__main__":
    main()




