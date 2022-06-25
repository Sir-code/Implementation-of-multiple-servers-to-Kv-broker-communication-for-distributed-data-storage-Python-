import socket
import threading


class Trie:
    head = {}

    def add(self, word):
        cur = self.head
        for ch in word:
            if ch not in cur:
                cur[ch] = {}
            cur = cur[ch]
        cur['*'] = True
        print(f" {word} is now in Trie")
        return "Done"

    def search(self, word):
        cur = self.head
        for ch in word:
            if ch not in cur:
                return False
            cur = cur[ch]
        if cur['*'] == True:
            return True
        return False

    def searchExact(self, word):
        cur = self.head
        for ch in word:
            if ch not in cur:
                return False
            cur = cur[ch]
        return True

    def delete(self, word):
        cur = self.head
        for ch in word:
            cur = cur[ch]
        cur["*"] = False


HEADER = 120
PORT = 7000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

receivedData = []
myTrie = Trie()


def handle_client(conn, addr):
    global receivedData
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")

            if msg[0:3] == "PUT":
                msg=str(msg)
                msg = eval(msg[4:len(msg)])

                def checkIfItIsalreadyThere(msg):
                    for allthings in receivedData:
                        if list(msg.keys())[0] in allthings.keys():
                            counter = 0
                            for allstuffs in range(len(receivedData)):
                                counter = counter + 1
                                for bbbss in receivedData[allstuffs]:
                                    if list(msg.keys())[0] == bbbss:
                                        print(type(receivedData))
                                        receivedData[counter - 1]=msg
                                        return True
                    return False

                if (checkIfItIsalreadyThere(msg) == True):
                    pass
                else:
                    receivedData.append(msg)
                    print("No it wasnt")
                    print(list(msg.keys())[0])
                    # print(receivedData)
                print("final output")
                print(len(receivedData))
                #print(receivedData)
                for j in receivedData:
                    for keys in j:
                        if (myTrie.search(keys) == False):
                            myTrie.add(keys)
                        else:
                            pass
                conn.send("Data uploaded to server 3".encode(FORMAT))

            elif msg[0:3] == "GET":
                msg=str(msg)
                if (msg[3] != " "):
                    conn.send("ERROR, Please leave space between the query and key/path".encode(FORMAT))
                elif "." in msg:
                    conn.send("ERROR, Please put in a valid form of QUERY, GET can access only high level keys".encode(FORMAT))
                elif myTrie.search(msg[4:len(msg)]) == True:
                    for j in receivedData:
                        for keys in j:
                            #print(keys)
                            if(msg[4:len(msg)]==keys):
                                j[keys] = str(j[keys])
                                conn.send(" :".join([msg[4:len(msg)], j[keys]]).encode(FORMAT))
                else:
                    conn.send("NOT FOUND, This data is not in server 3".encode(FORMAT))


            elif msg[0:5] == "QUERY":
                if (msg[5] != " "):
                    conn.send("ERROR, Please leave space between the query and key/path".encode(FORMAT))
                else:
                    message = msg[6:len(msg)]
                    lists = ""
                    result = []
                    for all in message:
                        if all != ".":
                            lists = lists + all
                        elif all == ".":
                            result.append(lists)
                            lists = ""
                    result.append(lists)
                    print(result)

                    def getPersonNumber():
                        counter = 0
                        for a in range(len(receivedData)):
                            counter = counter + 1
                            for b in receivedData[a]:
                                if b == result[0]:
                                    return counter - 1
                        return None
                    Locator = getPersonNumber()
                if Locator == None:
                    conn.send("NOT FOUND, This data is not in server 3, please put in a valid key or path".encode(FORMAT))
                else:
                    #print(getPersonNumber())
                    mo = str(Locator)
                    print(mo)
                    string = "receivedData" + "[" + mo + "]"
                    for i in result:
                        temps = str([i])
                        string = string + temps
                    #print(string)
                    #print(receivedData[2]['person3']['Age'])
                    try:
                        check =string
                        string = eval(string)
                        string = str(string)
                        print(string)
                        conn.send(" :".join([message, string]).encode(FORMAT))
                        print(type(receivedData))
                        print(receivedData[0])
                    except:
                        conn.send(check.encode(FORMAT))








            elif msg[0:6] == "DELETE":
                if (msg[6] != " "):
                    conn.send("ERROR, Please leave space between the query and key/path".encode(FORMAT))
                else:
                    message = msg[7:len(msg)]
                    results = str(message)

                    def getPersonNumbers():
                        counter = 0
                        for aa in range(len(receivedData)):
                            counter = counter + 1
                            for bat in receivedData[aa]:
                                print(bat)
                                if bat == results:
                                    return counter - 1
                        return None
                    location = getPersonNumbers()
                    if location is None:
                        print("Data is not in Server")
                        print(receivedData)
                        conn.send("NOT FOUND, Data is not in server 3".encode(FORMAT))
                    else:
                        receivedData.pop(location)
                        print(receivedData)
                        myTrie.delete(message)
                        conn.send(" ".join([msg[7:len(msg)]+" has been deleted from server 3", ""]).encode(FORMAT))

            elif msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                print("Please put in a valid Query, Options available are QUERY, GET, PUT and DELETE in capital letters")

    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server 1 is listening on {SERVER} on port {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
print("[STARTING]Server is Starting...")

start()
