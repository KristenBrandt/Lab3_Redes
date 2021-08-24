## Oliver Graf 17190
## Kristen Brandt 171482

#imports
import asyncio
import logging
import slixmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

#logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

class Client(ClientXMPP):
    def __init__(self, username, password):
        ClientXMPP.__init__(self, username, password)
        self.username_ = username
        self.password = password

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.register)


        # self.add_event_handler("groupchat_message", self.handleXMPPConnected.send_group_message)

    async def session_start(self, event):
        print("He entrado al chat exitosamente :)")
        self.send_presence()
        await self.get_roster()

        #registrarse en el servidor
    async def register(self, iq):
        print("AQUI")
        self.send_presence()
        self.get_roster()
        print("AQUI 2")

        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()






# Method to register a new user
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

# Method to login
def login(username, password):
    # Instance of the Client class to continue with the request in the async method
    client = Client(username, password)
    client.register_plugin("xep_0030")
    client.register_plugin("xep_0199")
    client.register_plugin('xep_0363')

    client.use_proxy = True
    client.proxy_config = {'host': 'alumchat.xyz','port': 5222}

    client.connect()
    client.process(forever=False)


dele = True
while dele:
    print("""Bienvenido porfavor ingrese que desea hacer:
    \t1.login
    \t2.signup
    \t3.salir""")


    option = int(input("Ingrese una opción para poder continuar: "))
    if option == 1:
        user = input("Usuario: ")
        password = input("Contraseña: ")
        register(user, password)

    elif option == 2:
        user = input("Usuario: ")
        password = input("Contraseña: ")
        login(user, password)

    elif option == 3:
        dele = False
    else:
        print("Invalid option")
