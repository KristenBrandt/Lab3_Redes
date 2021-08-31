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

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")
class Client(ClientXMPP):
    vecinos = {}
    # messages_recieved = []
    dvs = {}
    # G = nx.DiGraph()
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)



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

        def send_bellford():
            self.register_plugin("xep_0085")
            print("\nSending Bellman-Ford message\n")
            message = input("Message: ")
            reciever = input("Reciever: ")
            subject = reciever + " " + str(self.boundjid.user)
            calcs = {}
            for key in self.vecinos:
                calcs[key] = self.vecinos[key][reciever] + self.dvs[key]
            path = min(calcs, key=calcs.get)
            recipient = path+"@alumchat.xyz"
            self.send_message(mto=recipient, mbody=message, mtype="chat", msubject=subject)
            print("Enviado a " + recipient+ "\n")
            # self.messages_recieved.append(msg['subject'])








        menu_adentro = True
        while menu_adentro:
            print(self.boundjid.user)
            print("1. Chat\n2.Salir\n3.Send DVs\n4.Send Bellman-Ford message\n5.Listen\n6.Print DVs")

            opcion = int(input("Que opción desea: "))

            if opcion == 1:
                send_private_message()
            elif opcion == 2:
                self.send_presence(pshow="away", pstatus="Offline")
                self.disconnect()
                menu_adentro = False
            elif opcion == 3:
                self.send_dvs()
            elif opcion == 4:
                send_bellford()
            elif opcion == 5:
                print("I  am  listening! ")
                time.sleep(4)
            elif opcion == 6:
                print(self.dvs)

            await self.get_roster()

    def calculate_new_dvs(self):
        hubo_cambio = False
        for okey in self.vecinos:
            for key in self.vecinos[okey]:
                if key in self.dvs:
                    if self.dvs[key] > self.vecinos[okey][key] + self.dvs[okey]:
                        self.dvs[key] = self.vecinos[okey][key] + self.dvs[okey]
                        hubo_cambio = True
                else:
                    self.dvs[key] = self.dvs[okey] + self.vecinos[okey][key]

        return hubo_cambio

    def send_dvs(self):
        self.register_plugin("xep_0085")
        print("\nSending updated DVs\n")
        subject = "DVS"
        message = ""
        for key in self.dvs:
            message = message + key + ";"
            message = message + str(self.dvs[key]) + " "
        print(message)
        for key in self.vecinos:
            recipient = key + "@alumchat.xyz"
            self.send_message(mto=recipient, mbody=message, mtype="chat", msubject=subject)
            print("Enviado a " + recipient+ "\n")

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            sublist = msg['subject'].split()
            print(sublist)
            if "DVS" in msg['subject']:
                fr = str(msg['from']).split("@")[0]
                print("\nDVs update recieved from " + fr+ "\n")

                dvvvvs = str(msg['body']).split()

                dv2 = {}

                for i in range(len(dvvvvs)):
                    l = dvvvvs[i].split(";")
                    dv2[l[0]] = int(l[1])


                self.vecinos[fr] = dv2.copy()
                if self.calculate_new_dvs():
                    print("Hubo cambio en los DVs, enviando DVs a vecinos")
                    self.send_dvs()
            # elif msg['subject'] in self.messages_recieved:
            #     print('El mensaje flood con este subject: ' + msg['subject'] + ' ya habia sido recibido antes!\n')
            elif str(self.boundjid.user) in sublist[0]:
                print("\nMensaje Bellman-Ford recibido exitosamente!\n" + "\nMensaje: " +msg['body'] + "\n")
            else:
                print("\nReenviando mensaje Bellman-Ford\n")
                calcs = {}
                reciever = sublist[0]
                for key in self.vecinos:
                    calcs[key] = self.vecinos[key][reciever] + self.dvs[key]
                path = min(calcs, key=calcs.get)
                recipient = path+"@alumchat.xyz"
                self.send_message(mto=recipient, mbody=msg['body'], mtype="chat", msubject=subject)
                print("\nReenviado a " + recipient+ "\n")
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
    recvec = True

    while recvec:
        client.dvs[client.boundjid.user] = 0
        print("1. Ingresar un nodo vecino\n2. Continuar")
        oooo = input()
        if oooo == "1":
            vec = input("Ingrese el nombre de usuario del vecino: ")
            client.vecinos[vec] = {}
            dist = int(input("Ingrese la distancia hacia el vecino: "))
            client.dvs[vec] = dist
        elif oooo == "2":
            recvec = False
            print("Continuando... ")


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


        option = int(input("Ingrese una opción para poder continuar: "))
        if option == 2:
            user = input("Usuario: ")
            password = input("Contraseña: ")
            register(user, password)

        elif option == 1:
            user = input("Usuario: ")
            password = input("Contraseña: ")
            login(user, password)

        elif option == 3:
            dele = False
        else:
            print("Invalid option")
