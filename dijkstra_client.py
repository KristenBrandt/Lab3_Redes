#Oliver Graf 17190
# Kristen Brandt 171482

import asyncio
import logging
import uuid
import time
import networkx as nx
import sys
import aiodns
import asyncio

if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from slixmpp import ClientXMPP

# logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")
class Client(ClientXMPP):
    vecinos = []
    # messages_recieved = []
    tups = []
    G = nx.DiGraph()
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        #Open txt file containing graph data and populate netowrkx graph
        f = open("grafo.txt", "r")
        for x in f:
            l = x.split()
            l[2] = int(l[2])
            self.tups.append(tuple(l))

        self.G.add_weighted_edges_from(self.tups)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration

    async def session_start(self, event):
        print("He entrado al chat exitosamente :)")
        # print(self.boundjid.user)
        self.send_presence(pshow= "chat", pstatus="Available")
        self.get_roster()

        def send_private_message():
            self.register_plugin("xep_0085")

            recipient = input("Recipient: ")
            #notification(recipient, "typing")
            message = input("Message: ")
            subject = input("Subject: ")
            self.send_message(mto=recipient, mbody=message, mtype="chat", msubject=subject)
            #notification(recipient, "paused")
            print("Message sent!")

        def send_dijkstra():
            self.register_plugin("xep_0085")
            print("\nSending Dijkstra message\n")
            message = input("Message: ")
            reciever = input("Reciever: ")
            subject = reciever + " " + str(self.boundjid.user)
            path = nx.dijkstra_path(self.G,self.boundjid.user, reciever)
            path_print = []
            for i in range(len(path)):
                if i != (len(path) - 1):
                    path_print.append(path[i] +  " -> ")
                else:
                    path_print.append(path[i])
            path_arrow = [" "] * len(path)
            for i in range(len(path)):
                if self.boundjid.user in path[i]:
                    path_arrow[i] = "v"
                    matrix = [path_arrow, path_print]
                    s = [[str(e) for e in row] for row in matrix]
                    lens = [max(map(len, col)) for col in zip(*s)]
                    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
                    table = [fmt.format(*row) for row in s]
                    print ('\n'.join(table))
                    recipient = path[i+1] + "@alumchat.xyz"
                    self.send_message(mto=recipient, mbody=message, mtype="chat", msubject=subject)
                    print("Enviado a " + recipient+ "\n")
            # self.messages_recieved.append(msg['subject'])



        menu_adentro = True
        while menu_adentro:
            print(self.boundjid.user)
            print("1. Chat\n2.Salir\n3.Send Dijkstra\n4.Listen")

            opcion = int(input("Que opci??n desea: "))

            if opcion == 1:
                send_private_message()
            elif opcion == 2:
                self.send_presence(pshow="away", pstatus="Offline")
                self.disconnect()
                menu_adentro = False
            elif opcion == 3:
                send_dijkstra()
            elif opcion == 4:
                print("I  am  listening! ")
                time.sleep(1)

            await self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            sublist = msg['subject'].split()
            print(sublist)
            if str(self.boundjid.user) in sublist[0]:
                path = nx.dijkstra_path(self.G, sublist[1] , sublist[0])
                path_print = []
                for i in range(len(path)):
                    if i != (len(path) - 1):
                        path_print.append(path[i] +  " -> ")
                    else:
                        path_print.append(path[i])
                path_arrow = [" "] * len(path)
                path_arrow[len(path_arrow)-1] = "v"
                matrix = [path_arrow, path_print]
                s = [[str(e) for e in row] for row in matrix]
                lens = [max(map(len, col)) for col in zip(*s)]
                fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
                table = [fmt.format(*row) for row in s]
                print ('\n'.join(table))
                print("Mensaje Dijkstra recibido exitosamente!\n" + "\nMensaje: " +msg['body'] + "\n")
            # elif msg['subject'] in self.messages_recieved:
            #     print('El mensaje flood con este subject: ' + msg['subject'] + ' ya habia sido recibido antes!\n')
            else:

                path = nx.dijkstra_path(self.G, sublist[1] , sublist[0])
                path_print = []
                for i in range(len(path)):
                    if i != (len(path) - 1):
                        path_print.append(path[i] +  " -> ")
                    else:
                        path_print.append(path[i])
                path_arrow = [" "] * len(path)

                for i in range(len(path)):
                    if self.boundjid.user in path[i]:
                        path_arrow[i] = "v"
                        matrix = [path_arrow, path_print]
                        s = [[str(e) for e in row] for row in matrix]
                        lens = [max(map(len, col)) for col in zip(*s)]
                        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
                        table = [fmt.format(*row) for row in s]
                        print ('\n'.join(table))
                        recipient = path[i+1] + "@alumchat.xyz"
                        self.send_message(mto=recipient, mbody=msg['body'], mtype="chat", msubject=msg['subject'])
                        print("\nMensaje Dijkstra reenviado a " + recipient+ "\n")
            # self.messages_recieved.append(msg['subject'])
            #msg.reply("Thanks for sending\n%(subject)s" % msg).send()
        #print("Mensaje enviado %(subject)s " % msg)


    async def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print("Cuenta creada")
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            print("Error al crear cuenta")
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("Error al crear cuenta")
            logging.error("No response from server.")
            self.disconnect()



def register(username, password):
    client = Client(username, password)
    client.use_proxy = True
    client.proxy_config = {'host': 'alumchat.xyz','port': 5222}

    client.register_plugin("xep_0030")
    client.register_plugin("xep_0004")
    client.register_plugin("xep_0199")
    client.register_plugin("xep_0066")
    client.register_plugin("xep_0077")

    # We force the registration
    client["xep_0077"].force_registration = True

    client.connect()
    client.process()

def login(username, password):
    # Instance of the Client class to continue with the request in the async method
    client = Client(username, password)
    #client.disconnect()
    client.use_proxy = True
    client.proxy_config = {'host': 'alumchat.xyz','port': 5222}
    # recvec = True

    # while recvec:
    #     print("1. Ingresar un nodo vecino\n2. Continuar")
    #     oooo = input()
    #     if oooo == "1":
    #         vec = input("Ingrese el nombre de usuario del vecino: ")
    #         client.vecinos.append(vec)
    #     elif oooo == "2":
    #         recvec = False
    #         print("Continuando... ")


    client.register_plugin("xep_0030")
    client.register_plugin("xep_0199")
    client.register_plugin('xep_0363')

    client.connect()
    client.process(forever=False)


if __name__ == '__main__':
    dele = True
    while dele:
        print("""Bienvenido porfavor ingrese que desea hacer:
        \t1.login
        \t2.signup
        \t3.salir""")


        option = int(input("Ingrese una opci??n para poder continuar: "))
        if option == 2:
            user = input("Usuario: ")
            password = input("Contrase??a: ")
            register(user, password)

        elif option == 1:
            user = input("Usuario: ")
            password = input("Contrase??a: ")
            login(user, password)

        elif option == 3:
            dele = False
        else:
            print("Invalid option")
